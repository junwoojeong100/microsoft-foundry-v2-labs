import json
import os
import unittest
from dataclasses import replace
from unittest.mock import patch

import httpx
from agent_framework import Agent
from azure.ai.projects.aio import AIProjectClient
from azure.core.credentials import AccessToken

from foundry_workshop.profiles import RuntimeProfile, runtime_contract
from foundry_workshop.runtime import inference_client

from .test_sdk_contracts import ROOT, response_body, settings


class AsyncCredential:
    def __init__(self):
        self.scopes = []

    async def get_token(self, *scopes, **_kwargs):
        self.scopes.extend(scopes)
        return AccessToken("unit-test-not-a-real-token", 4102444800)

    async def close(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        await self.close()


class InferenceModeTests(unittest.IsolatedAsyncioTestCase):
    async def test_both_explicit_apis_use_real_sdk_paths_and_correct_audiences(self):
        for api in ("project-responses", "account-chat"):
            with (
                self.subTest(api=api),
                patch.dict(os.environ, {"OTEL_SDK_DISABLED": "true"}, clear=True),
            ):
                captured = []
                credential = AsyncCredential()
                config = replace(settings(), openai_endpoint="https://unit.openai.azure.com")
                original = AIProjectClient.get_openai_client

                def handle(request, _captured=captured, _api=api):
                    _captured.append((request.url, json.loads(request.content)))
                    if _api == "project-responses":
                        return httpx.Response(200, json=response_body("unit answer"))
                    return httpx.Response(
                        200,
                        json={
                            "id": "chatcmpl-unit",
                            "object": "chat.completion",
                            "created": 1789257600,
                            "model": "unit-model",
                            "choices": [
                                {
                                    "index": 0,
                                    "finish_reason": "stop",
                                    "message": {"role": "assistant", "content": "unit answer"},
                                }
                            ],
                            "usage": {
                                "prompt_tokens": 10,
                                "completion_tokens": 20,
                                "total_tokens": 30,
                            },
                        },
                    )

                def owned_client(project, _original=original, _handle=handle, **kwargs):
                    kwargs["http_client"] = httpx.AsyncClient(
                        transport=httpx.MockTransport(_handle)
                    )
                    kwargs["max_retries"] = 0
                    return _original(project, **kwargs)

                with patch("foundry_workshop.runtime.credential_for", return_value=credential):
                    with patch.object(AIProjectClient, "get_openai_client", owned_client):
                        async with inference_client(config, RuntimeProfile(api=api)) as client:
                            result = await Agent(client=client, instructions="unit only").run(
                                "unit question"
                            )
                self.assertEqual(result.text, "unit answer")
                self.assertEqual(len(captured), 1)
                expected = (
                    "/api/projects/workshop/openai/v1/responses"
                    if api == "project-responses"
                    else "/openai/v1/chat/completions"
                )
                self.assertEqual(captured[0][0].path, expected)
                self.assertEqual(captured[0][1]["model"], config.deployment)
                scope = (
                    "https://ai.azure.com/.default"
                    if api == "project-responses"
                    else "https://cognitiveservices.azure.com/.default"
                )
                self.assertIn(scope, credential.scopes)

    async def test_account_endpoint_mismatch_fails_before_credentials_or_network(self):
        with patch.dict(os.environ, {}, clear=True):
            config = replace(settings(), openai_endpoint="https://other.openai.azure.com")
            profile = RuntimeProfile(api="account-chat", protocol="invocations")
            with self.assertRaises(ValueError):
                runtime_contract(ROOT, config, profile)
            with patch("foundry_workshop.runtime.credential_for") as credential:
                with self.assertRaises(ValueError):
                    async with inference_client(config, profile):
                        self.fail("A mismatched account must not be called.")
                credential.assert_not_called()

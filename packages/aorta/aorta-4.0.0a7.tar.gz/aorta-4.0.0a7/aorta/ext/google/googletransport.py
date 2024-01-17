# Copyright (C) 2020-2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`GoogleTransport`."""
import os
from typing import Any

from aorta.types import Envelope
from .pubsubtransport import PubsubTransport
import fastapi


class GoogleTransport(PubsubTransport):
    prefix: str
    service_name: str

    def __init__(
        self,
        project: str = fastapi.Depends(lambda: os.environ['GOOGLE_SERVICE_PROJECT']),
        prefix: str = fastapi.Depends(lambda: os.environ['AORTA_CHANNEL_PREFIX']),
        service_name: str = fastapi.Depends(lambda: os.environ['APP_NAME'])
    ):
        self.prefix = prefix
        self.service_name = service_name
        super().__init__(
            project=project,
            topic=self.topic_factory,
            retry_topic=f'{self.prefix}.retry.{service_name}'
        )

    def topic_factory(self, envelope: Envelope[Any]) -> list[str]:
        if envelope.is_event():
            topics: list[str] = [
                f'{self.prefix}.events.{envelope.kind}'
            ]
            if not envelope.is_private_event():
                topics.append(f'{self.prefix}.events')
        elif envelope.is_command():
            topics = [f'{self.prefix}.commands.{self.service_name}']
            if envelope.metadata.audience:
                topics = [
                    f'{self.prefix}.commands.{x}' if x != 'self'\
                    else f'{self.prefix}.commands.{self.service_name}'
                    for x in envelope.metadata.audience
                    if x != 'self'
                ]
        else:
            raise NotImplementedError
        return topics
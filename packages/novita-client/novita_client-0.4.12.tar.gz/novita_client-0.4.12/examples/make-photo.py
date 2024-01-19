#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from novita_client import NovitaClient
import base64


client = NovitaClient(os.getenv('NOVITA_API_KEY'), os.getenv('NOVITA_API_URI', None))

res = client.make_photo(
    model_name="protovisionXLHighFidelity3D_releaseV660Bakedvae_207131.safetensors",
    prompt="instagram photo, portrait photo of a woman img, colorful, perfect face, natural skin, hard shadows, film grain",
    images=[
        "scarlett_0.jpg"
    ],
    steps=20,
    guidance_scale=5,
    image_num=1,
    strength=0.5,
    seed=-1,
)


for idx in range(len(res.images_encoded)):
    with open(f"make_photo_{idx}.png", "wb") as f:
        f.write(base64.b64decode(res.images_encoded[idx]))

from novita_client import NovitaClient
import gradio as gr


import requests
from io import BytesIO
from PIL import Image, ImageOps
import base64
import os
import logging


def base64_to_image(base64_image: str) -> Image:
    # convert base64 string to image
    image = Image.open(BytesIO(base64.b64decode(base64_image)))
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB")


def image_to_base64(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('ascii')


def get_noviata_client(novita_key):
    client = NovitaClient(novita_key, os.getenv('NOVITA_API_URI', None))
    client.set_extra_headers({"User-Agent": "stylization-playground"})
    return client


get_local_storage = """
    function() {
      globalThis.setStorage = (key, value)=>{
        localStorage.setItem(key, JSON.stringify(value))
      }
       globalThis.getStorage = (key, value)=>{
        return JSON.parse(localStorage.getItem(key))
      }

       const novita_key =  getStorage('novita_key')
       return [novita_key];
      }
    """


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            novita_key = gr.Textbox(value="", label="Novita.AI API KEY (store in broweser)", placeholder="novita.ai api key", type="password")

    with gr.Row():
        with gr.Column():
            with gr.Blocks():
                model = gr.Dropdown(choices=["epicrealism_pureEvolutionV5_97793.safetensors"], label="model")
                lora_model = gr.Dropdown(choices=[], label="lora model", type="index", allow_custom_value=True)
                # lora_model = gr.Dropdown(choices=["model_1702891607_98D820C897.safetensors"], label="lora model", allow_custom_value=True)
                lora_strength = gr.Slider(label="lora strength", value=0.7, step=0.1, minimum=0.1, maximum=1.0)
                height = gr.Slider(label="height", value=512, step=1, minimum=256, maximum=1024)
                width = gr.Slider(label="width", value=512, step=1, minimum=256, maximum=1024)
                steps = gr.Slider(label="steps", value=20, step=1, minimum=1, maximum=100)
                _hide_lora_training_response = gr.JSON(visible=False)

            with gr.Tab(label="1st Condition"):
                prompt_1 = gr.Text(label="prompt")
                controlnet_model_1 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_1 = gr.Image(label="controlnet image", type="pil")
                num_frames_1 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)

            with gr.Tab(label="2st Condition"):
                prompt_2 = gr.Text(label="prompt")
                controlnet_model_2 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_2 = gr.Image(label="controlnet image", type="pil")
                num_frames_2 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)

            with gr.Tab(label="3st Condition"):
                prompt_3 = gr.Text(label="prompt")
                controlnet_model_3 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_3 = gr.Image(label="controlnet image", type="pil")
                num_frames_3 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)

            with gr.Tab(label="4st Condition"):
                prompt_4 = gr.Text(label="prompt")
                controlnet_model_4 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_4 = gr.Image(label="controlnet image", type="pil")
                num_frames_4 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)
            with gr.Tab(label="5st Condition"):
                prompt_5 = gr.Text(label="prompt")
                controlnet_model_5 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_5 = gr.Image(label="controlnet image", type="pil")
                num_frames_5 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)
            with gr.Tab(label="6st Condition"):
                prompt_6 = gr.Text(label="prompt")
                controlnet_model_6 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_6 = gr.Image(label="controlnet image", type="pil")
                num_frames_6 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)
            with gr.Tab(label="7st Condition"):
                prompt_7 = gr.Text(label="prompt")
                controlnet_model_7 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_7 = gr.Image(label="controlnet image", type="pil")
                num_frames_7 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)
            with gr.Tab(label="8st Condition"):
                prompt_8 = gr.Text(label="prompt")
                controlnet_model_8 = gr.Dropdown(["control_v11f1p_sd15_depth"], label="controlnet model")
                controlnet_image_8 = gr.Image(label="controlnet image", type="pil")
                num_frames_8 = gr.Slider(label="num frames", value=16, step=1, minimum=1, maximum=32)

        with gr.Column():
            inference_refresh_button = gr.Button(value="Refresh Subject LoRA")
            generate_button = gr.Button(value="Generate Video")

            with gr.Blocks() as output:
                output_video = gr.Video(label="output video")

            # trained_loras_models = [_.name for _ in get_noviata_client(novita_key).models_v3(refresh=True).filter_by_type("lora").filter_by_visibility("private")]
            def inference_refresh_button_fn(novita_key):
                try:
                    serving_models = [_.models[0].model_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                    serving_models_labels = [_.task_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                    default_serving_model = serving_models_labels[0] if len(serving_models_labels) > 0 else None
                except Exception as e:
                    logging.error(e)
                    return novita_key, gr.update(choices=[], value=None), gr.update(value=None), f"$ UNKNOWN", gr.update(visible=False)

                return novita_key, gr.update(choices=serving_models_labels, value=default_serving_model), serving_models

            inference_refresh_button.click(
                inputs=[novita_key],
                outputs=[novita_key, lora_model, _hide_lora_training_response],
                fn=inference_refresh_button_fn
            )

            def generate_video(
                model,
                lora_model,
                lora_strength,
                width,
                height,
                steps,
                _hide_lora_training_response,
                prompt_1,
                controlnet_model_1,
                controlnet_image_1,
                num_frames_1,
                prompt_2,
                controlnet_model_2,
                controlnet_image_2,
                num_frames_2,
                prompt_3,
                controlnet_model_3,
                controlnet_image_3,
                num_frames_3,
                prompt_4,
                controlnet_model_4,
                controlnet_image_4,
                num_frames_4,
                prompt_5,
                controlnet_model_5,
                controlnet_image_5,
                num_frames_5,
                prompt_6,
                controlnet_model_6,
                controlnet_image_6,
                num_frames_6,
                prompt_7,
                controlnet_model_7,
                controlnet_image_7,
                num_frames_7,
                prompt_8,
                controlnet_model_8,
                controlnet_image_8,
                num_frames_8,
            ):
                address = os.environ.get("DIFFUSIONGRID_API_ADDRESS", "http://localhost:8860")

                if isinstance(lora_model, int):
                    lora_model = _hide_lora_training_response[lora_model].replace(".safetensors", "")
                else:
                    lora_model = lora_model.replace(".safetensors", "")

                req_body = {
                    "model": model,
                    "height": height,
                    "width": width,
                    "negative_prompt": "bad quality",
                    "loras": [
                        {
                            "model": lora_model,
                            "scale": lora_strength,
                        },
                    ],
                    "steps": steps,
                    "conditions": [],
                }

                if prompt_1:
                    req_body["conditions"].append({
                        "prompt": prompt_1,
                        "frames": num_frames_1,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_1,
                                "image": image_to_base64(controlnet_image_1),
                            }
                        ]
                    })
                if prompt_2:
                    req_body["conditions"].append({
                        "prompt": prompt_2,
                        "frames": num_frames_2,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_2,
                                "image": image_to_base64(controlnet_image_2),
                            }
                        ]
                    })
                if prompt_3:
                    req_body["conditions"].append({
                        "prompt": prompt_3,
                        "frames": num_frames_3,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_3,
                                "image": image_to_base64(controlnet_image_3),
                            }
                        ]
                    })
                if prompt_4:
                    req_body["conditions"].append({
                        "prompt": prompt_4,
                        "frames": num_frames_4,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_4,
                                "image": image_to_base64(controlnet_image_4),
                            }
                        ]
                    })
                if prompt_5:
                    req_body["conditions"].append({
                        "prompt": prompt_5,
                        "frames": num_frames_5,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_5,
                                "image": image_to_base64(controlnet_image_5),
                            }
                        ]
                    })

                if prompt_6:
                    req_body["conditions"].append({
                        "prompt": prompt_6,
                        "frames": num_frames_6,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_6,
                                "image": image_to_base64(controlnet_image_6),
                            }
                        ]
                    })
                if prompt_7:
                    req_body["conditions"].append({
                        "prompt": prompt_7,
                        "frames": num_frames_7,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_7,
                                "image": image_to_base64(controlnet_image_7),
                            }
                        ]
                    })
                if prompt_8:
                    req_body["conditions"].append({
                        "prompt": prompt_8,
                        "frames": num_frames_8,
                        "controlnet_units": [
                            {
                                "model": controlnet_model_8,
                                "image": image_to_base64(controlnet_image_8),
                            }
                        ]
                    })

                res = requests.post(
                    f"{address}/api/control2video",
                    json=req_body,
                )

                import tempfile
                with tempfile.NamedTemporaryFile(delete=False) as file:
                    file.write(base64.b64decode(res.json()["video"]))
                return file.name

            generate_button.click(
                fn=generate_video,
                inputs=[
                    model,
                    lora_model,
                    lora_strength,
                    width,
                    height,
                    steps,
                    _hide_lora_training_response,
                    prompt_1,
                    controlnet_model_1,
                    controlnet_image_1,
                    num_frames_1,
                    prompt_2,
                    controlnet_model_2,
                    controlnet_image_2,
                    num_frames_2,
                    prompt_3,
                    controlnet_model_3,
                    controlnet_image_3,
                    num_frames_3,
                    prompt_4,
                    controlnet_model_4,
                    controlnet_image_4,
                    num_frames_4,
                    prompt_5,
                    controlnet_model_5,
                    controlnet_image_5,
                    num_frames_5,
                    prompt_6,
                    controlnet_model_6,
                    controlnet_image_6,
                    num_frames_6,
                    prompt_7,
                    controlnet_model_7,
                    controlnet_image_7,
                    num_frames_7,
                    prompt_8,
                    controlnet_model_8,
                    controlnet_image_8,
                    num_frames_8,
                ],
                outputs=[
                    output_video
                ]
            )

    with gr.Row():
        def mirror(*args):
            return args

        with gr.Row():
            examples = gr.Examples(
                [
                    # [
                    #     "epicrealism_pureEvolutionV5_97793.safetensors",
                    #     "model_1702295117_31F9F902C5.safetensors",
                    #     0.7,
                    #     512,
                    #     512,
                    #     20,
                    #     "a closeup photo of a ohwx child, 5 years old, portrait",
                    #     "control_v11f1p_sd15_depth",
                    #     "./child-depth.png",
                    #     16,
                    #     "a closeup photo of a ohwx teen, 10 years old, portrait",
                    #     "control_v11f1p_sd15_depth",
                    #     "./man-depth.png",
                    #     16,
                    #     "a closeup photo of a ohwx man, 30 years old, portrait",
                    #     "control_v11f1p_sd15_depth",
                    #     "./man-depth.png",
                    #     16,
                    #     "a closeup photo of a ohwx old man, 50 years old, white hair, portrait",
                    #     "control_v11f1p_sd15_depth",
                    #     "./man-depth.png",
                    #     16,
                    # ]
                    [
                        "epicrealism_pureEvolutionV5_97793.safetensors",
                        "model_1702891607_98D820C897.safetensors",
                        0.6,
                        512,
                        768,
                        20,
                        "Detailed and realistic portrait of a ohwx 5-year-old baby, (baby_face), cute, chubby_cheek:1.5, rosy_cheek, (big_eyes), round_nose, small_mouth, short_face, kid_clothes, smile, sparse_eyebrows, thin_hair, grey_background, headshot photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 15-year-old kid, cute, chubby_cheek, rosy_cheek, round_nose, kid_clothes, smile, grey_background, headshot photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 25-year-old kid, cute, chubby_cheek, rosy_cheek, round_nose, kid_clothes, smile, grey_background, headshot photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 35 year old woman with freckles, round eyes and short messy hair shot outside, realistic, photorealistic, vibrant colors, symmetrical face, glistening skin, volumetric lighting, soft natural lighting, portrait photography, 85mm lens, magical photography, photo realism, ultra-detailed, portrait composition, 8k,",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 45 year old woman with freckles, round eyes and short messy hair shot outside, realistic, photorealistic, vibrant colors, symmetrical face, glistening skin, volumetric lighting, soft natural lighting, portrait photography, 85mm lens, magical photography, photo realism, ultra-detailed, portrait composition, 8k,",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 55-year-old woman, old_woman, elderly, (wrinkles:1.5), smile, grey_hair, (aging_face), age_spots, ((wrinkled_face)), bagging_skin, fine lines, (crow's-feet), (nasolabialis_folds), sagging_skin, (wrinkled_forehead), (elderly_clothing), elderly_hairstyle, ((grey_background)), looking_at_viewer, warm, peaceful, kind, ultra-detailed, digital art, headshot photography, intricate details, studio lighting, depth of field, portrait photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 65-year-old woman, old_woman, elderly, (wrinkles:1.5), smile, grey_hair, (aging_face), age_spots, ((wrinkled_face)), bagging_skin, fine lines, (crow's-feet), (nasolabialis_folds), sagging_skin, (wrinkled_forehead), (elderly_clothing), elderly_hairstyle, ((grey_background)), looking_at_viewer, warm, peaceful, kind, ultra-detailed, digital art, headshot photography, intricate details, studio lighting, depth of field, portrait photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                        "Detailed and realistic portrait of a ohwx 75-year-old woman, old_woman, elderly, (wrinkles:1.5), smile, grey_hair, (aging_face), age_spots, ((wrinkled_face)), bagging_skin, fine lines, (crow's-feet), (nasolabialis_folds), sagging_skin, (wrinkled_forehead), (elderly_clothing), elderly_hairstyle, ((grey_background)), looking_at_viewer, warm, peaceful, kind, ultra-detailed, digital art, headshot photography, intricate details, studio lighting, depth of field, portrait photography, 85mm lens, photo realism, ultra-detailed, portrait composition, 8k",
                        "control_v11f1p_sd15_depth",
                        "./woman-depth.png",
                        8,
                    ]
                ],
                [
                    model,
                    lora_model,
                    lora_strength,
                    width,
                    height,
                    steps,
                    prompt_1,
                    controlnet_model_1,
                    controlnet_image_1,
                    num_frames_1,
                    prompt_2,
                    controlnet_model_2,
                    controlnet_image_2,
                    num_frames_2,
                    prompt_3,
                    controlnet_model_3,
                    controlnet_image_3,
                    num_frames_3,
                    prompt_4,
                    controlnet_model_4,
                    controlnet_image_4,
                    num_frames_4,
                    prompt_5,
                    controlnet_model_5,
                    controlnet_image_5,
                    num_frames_5,
                    prompt_6,
                    controlnet_model_6,
                    controlnet_image_6,
                    num_frames_6,
                    prompt_7,
                    controlnet_model_7,
                    controlnet_image_7,
                    num_frames_7,
                    prompt_8,
                    controlnet_model_8,
                    controlnet_image_8,
                    num_frames_8,
                ],
                [
                    model,
                    lora_model,
                    lora_strength,
                    width,
                    height,
                    steps,
                    prompt_1,
                    controlnet_model_1,
                    controlnet_image_1,
                    num_frames_1,
                    prompt_2,
                    controlnet_model_2,
                    controlnet_image_2,
                    num_frames_2,
                    prompt_3,
                    controlnet_model_3,
                    controlnet_image_3,
                    num_frames_3,
                    prompt_4,
                    controlnet_model_4,
                    controlnet_image_4,
                    num_frames_4,
                    prompt_5,
                    controlnet_model_5,
                    controlnet_image_5,
                    num_frames_5,
                    prompt_6,
                    controlnet_model_6,
                    controlnet_image_6,
                    num_frames_6,
                    prompt_7,
                    controlnet_model_7,
                    controlnet_image_7,
                    num_frames_7,
                    prompt_8,
                    controlnet_model_8,
                    controlnet_image_8,
                    num_frames_8
                ],
                mirror,
                cache_examples=False,
            )

        novita_key.change(inference_refresh_button_fn, inputs=novita_key, outputs=[novita_key, lora_model, _hide_lora_training_response], js="(v)=>{ setStorage('novita_key',v); return [v]; }")

        demo.load(
            inputs=[novita_key],
            outputs=[novita_key, lora_model, _hide_lora_training_response],
            fn=inference_refresh_button_fn,
            js=get_local_storage,
        )

demo.launch(server_name="0.0.0.0", server_port=8233)

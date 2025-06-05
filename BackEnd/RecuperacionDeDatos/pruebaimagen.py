from diffusers import StableDiffusionPipeline
import torch

# Token personal de Hugging Face
HUGGINGFACE_TOKEN = "api_token"


# Inicializa la pipeline una sola vez (puedes cambiar "cuda" por "cpu" si no tienes GPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1"
).to("cpu")


def generar_prompt_visual(nombre_comun=None, nombre_cientifico=None):
    base_prompt = "A realistic, high resolution photograph of "

    if nombre_comun and nombre_cientifico:
        base_prompt += f"a {nombre_comun} ({nombre_cientifico}), "
    elif nombre_comun:
        base_prompt += f"a {nombre_comun}, "
    elif nombre_cientifico:
        base_prompt += f"a {nombre_cientifico}, "
    else:
        base_prompt += "an endangered species, "

    base_prompt += (
        "an endangered animal from Boyacá, Colombia, "
        "in its natural habitat, "
        "National Geographic style, "
        "cinematic lighting, "
        "vibrant colors, "
        "photo-realistic"
    )

    return base_prompt


def generar_imagen_desde_prompt(prompt, nombre_archivo="output.png"):
    # Genera la imagen con el prompt dado
    imagen = pipe(prompt).images[0]
    # Guarda la imagen en disco
    imagen.save(nombre_archivo)
    return nombre_archivo



if __name__ == "__main__":
    prompt = generar_prompt_visual(nombre_comun="guacamayo azul", nombre_cientifico="Anodorhynchus hyacinthinus")
    archivo = generar_imagen_desde_prompt(prompt, "guacamayo.png")
    print(f"Imagen generada y guardada en {archivo}")

from diffusers import StableDiffusionPipeline
import torch

# Token personal de Hugging Face
HUGGINGFACE_TOKEN = "api_token"


# Inicializa la pipeline una sola vez (puedes cambiar "cuda" por "cpu" si no tienes GPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1"
).to("cpu")


def generar_prompt_visual(nombre_comun=None, nombre_cientifico=None, descripcion_visual=None):
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
    descripcion = (
    "A small nocturnal frog, approximately 3 cm in size, known as Allobates juanii, "
    "resting on a damp forest floor in Boyacá, Colombia. It has dark brown skin with a shiny appearance, "
    "featuring irregular green and light beige stripes and spots running along its back and sides. "
    "Its legs are orange-pinkish and speckled, with a slightly translucent glow. "
    "The frog's posture is alert, sitting among fallen leaves and moist earth. "
    "Soft cinematic lighting highlights its moist texture, with shallow depth of field, "
    "vibrant but natural colors, photo-realistic style, National Geographic quality."
 )
    prompt = generar_prompt_visual(
        nombre_comun="Rana venenosa", 
        nombre_cientifico="Allobates juanii",
        descripcion_visual=descripcion)
    
    
    
    archivo = generar_imagen_desde_prompt(prompt, "AllobatesJuanii2.png")
    print(f"Imagen generada y guardada en {archivo}")

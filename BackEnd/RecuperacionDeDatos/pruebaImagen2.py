import requests

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/ultra",
    headers={
        "authorization": "Bearer sk-mflNusCgKEVo4opk6uwxhnD5JwP2DbhYS3qIoEw22QQTpyxj",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": (
            "A small nocturnal frog, approximately 3 cm in size, known as Allobates juanii, " 
            "resting near the base of the Eiffel Tower in Paris, France, on a damp patch of earth and moss among urban greenery. "
            "It has dark brown skin with a shiny appearance, "
            "featuring irregular green and light beige stripes and spots running along its back and sides. "
            "Its legs are orange-pinkish and speckled, with a slightly translucent glow. "
            "The frog's posture is alert, sitting beside small fallen leaves and moist soil under the iconic iron structure. "
            "Soft cinematic lighting highlights its moist texture, with shallow depth of field, "
            "vibrant but natural colors, photo-realistic style, National Geographic quality."
        ),
        "output_format": "webp",
    },
)

if response.status_code == 200:
    with open("allobates_juaniiTres.webp", 'wb') as file:
        file.write(response.content)
    print("Imagen generada exitosamente.")
else:
    raise Exception(str(response.json()))

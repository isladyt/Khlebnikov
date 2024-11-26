def convert_image_to_blob(image_path):
    #Конвертирование изображения в бинарный формат.
    with open(image_path, "rb") as file:
        blob = file.read()
    return blob

from db.manager import Manager as DBManager
import constants
import os
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
from db.models import TrainLogsModel

db_manager = DBManager(check_same_thread=False)


def check_images(front_image, back_image, left_image, right_image):
    if not front_image:
        return "L'image de l'avant de la voiture est requise."
    if not back_image:
        return "L'image de l'arrière de la voiture est requise."
    if not left_image:
        return "L'image du côté gauche de la voiture est requise."
    if not right_image:
        return "L'image du côté droit de la voiture est requise."
    return None


def get_car_part_detection_model():
    models_info = db_manager.select(
        TrainLogsModel.get_table_name(TrainLogsModel),
        columns=["path"],
        filters="completed='True'",
        condition="ORDER BY id DESC LIMIT 1",
        verbose=True
    )
    print(models_info)
    model_info = models_info[0] if models_info else None
    
    if model_info is None:
        return {"error": "Aucun modèle n'a été trouvé."}

    model_path = os.path.join(model_info["path"], "last.pt")

    return model_path


def confirm_parts(results, sides):
    # classes
    # back_bumper, back_glass, back_left_door, back_left_light, back_right_door, back_right_light, front_bumper, front_glass, front_left_door, front_left_light, front_right_door, front_right_light, hood, left_mirror, right_mirror, tailgate, trunk (of trucks and SUVs), and wheel

    for res in results:
        print(res.probs)


def detect_car_part(*kwargs: list[tuple[str, str]]):
    model_path = get_car_part_detection_model()
    model = YOLO("yolo")
    sides = ["front", "back", "left", "right"]
    results = model([arg0 for arg0, arg1 in kwargs if arg0 and arg1 in sides])
    
    return confirm_parts(results, [arg1 for arg0, arg1 in kwargs if arg0 and arg1 in sides])


def predict(front_image, back_image, left_image, right_image, main_color, plate_number):
    """Prédire les caractéristiques de la voiture."""

    # if error := check_images(front_image, back_image, left_image, right_image):
    if error := check_images(front_image, 1, 1, 1):
        return error

    bytes_front_image = front_image.getvalue()
    # bytes_back_image = back_image.getvalue()
    # bytes_left_image = left_image.getvalue()
    # bytes_right_image = right_image.getvalue()
    
    # type bytes is not a supported Ultralytics prediction source type.
    # convert bytes to image
    
    
    right_front_image = Image.open(BytesIO(bytes_front_image))
    # right_back_image = Image.open(BytesIO(bytes_back_image))
    # right_left_image = Image.open(BytesIO(bytes_left_image))
    # right_right_image = Image.open(BytesIO(bytes_right_image))
    
    # show image
    right_front_image.show()
    
    # Prédire les caractéristiques de la voiture
    is_front = detect_car_part((right_front_image, "front"))
    # is_back = detect_car_part((bytes_back_image, "back"))
    # is_left = detect_car_part((bytes_left_image, "left"))
    # is_right = detect_car_part((bytes_right_image, "right"))

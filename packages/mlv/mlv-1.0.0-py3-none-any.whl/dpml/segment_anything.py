from PIL import Image
import numpy
from .util import timer


def cutout(origin, mask):
    import cv2

    image = cv2.imread(origin)
    mask = cv2.imread(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # add alpha channel
    new_img = cv2.cvtColor(masked_image, cv2.COLOR_BGR2BGRA)
    new_img[:, :, 3] = mask

    return Image.fromarray(new_img)


def segment(image, point=[], model_type="vit_b", checkpoint="sam_vit_b_01ec64.pth"):
    from segment_anything import (
        SamPredictor,
        SamAutomaticMaskGenerator,
        sam_model_registry,
    )

    image = numpy.asarray(Image.open(image))
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    with timer("segment inference"):
        if point and len(point):
            predictor = SamPredictor(sam)
            predictor.set_image(image)
            masks, _, _ = predictor.predict(
                point_coords=numpy.array(point),
                point_labels=numpy.array([1, 1]),
                multimask_output=False,
            )
            for i, mask in enumerate(masks):
                filename = f"{i}.png"
                Image.fromarray(mask).save("output/" + filename)

        else:
            generator = SamAutomaticMaskGenerator(sam)
            masks = generator.generate(image)
            for i, mask in enumerate(masks):
                bin = mask["segmentation"]
                filename = f"{i}.png"
                Image.fromarray(bin).save("output/" + filename)

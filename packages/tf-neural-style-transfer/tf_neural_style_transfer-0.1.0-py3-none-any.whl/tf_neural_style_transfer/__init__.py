import os

def execute(target_image_name, target_image_url, reference_image_name, reference_image_url):
    os.environ['TARGET_IMAGE_NAME'] = target_image_name
    os.environ['TARGET_IMAGE_URL'] = target_image_url
    os.environ['REFERENCE_IMAGE_NAME'] = reference_image_name
    os.environ['REFERENCE_IMAGE_URL'] = reference_image_url

    import tf_neural_style_transfer.execute

import boto3


def detectTextIA(photo):
    access_key_id = ''
    secret_access_key = ''

    try:
        
        client = boto3.client('rekognition', 'us-east-2',
                              aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_access_key)
    except Exception as errors:
        print(f"Error client: {errors}")
        print('Client set error')

    try:
        
        response = client.detect_text(Image={'Bytes': photo})
        
    except Exception as errors:
        print(f"Error image: {errors}")
        print('Photo set error')
        return


    
    detected = ''                     
    textDetections=response['TextDetections']
    
    for text in textDetections:
            detected = detected + text['DetectedText'] + '\n' 
    
    return detected

def checkIA(file):

    photo=''

    with open(file, 'rb') as source_image:
        photo = source_image.read()

    r=detectTextIA(photo)
    print("Text detected: " + str(r))
    return r

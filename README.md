# Secure-Bell

Smart doorbell with facial recognition to recognise strangers approaching house.

## Planned implementation

- Facial recognition using OpenCV.
- Library of house members to compare new faces to.
- Passive scanning: Camera records and stores footage whenever it detects non-recognized person.
- Text alert to homeowner.

## Implementation Notes

- Building facial recognition database.
  - Need to have server to update additions to library.
  - Write code to update changes.
  
- Use Raspberry Pi as webcam to external server.
  - Server to centralise GPU calculations and facial recognition.

- Build Swift app to take pictures to upload.

## Built With

- Python
- OpenCV API

# Rock Paper Scissors CV

## Installation
## Front End
- The front end was created utilizing Angular v18. This application will require access to a webcam/camera.
- Run `npm install` to install dependencies. To run the front end, run `ng serve` or `npm start`.

## Back End
- The back end utilizes FastApi and Uvicorn running with OpenCV, GestureRecognizer, and Keras. Run `pip install -r requirements.txt` to install all dependencies. Then, run `main.py` to run the API client.
- Note: Inside the backend folder exists a notebook folder with two notebooks that are not used in the API calls/model prediction.
  - `main.ipynb` utilizes the OpenCV capture and the hand prediction can be done locally.
  -  `crop.ipynb` uses GestureRecognizer to crop out hands from a dataset, which was used to train the model. This code is not part of anything running in the model prediction.

## Instructions
- Raise a hand up and choose a paper, scissors, or rock form with it. Click `Take Picture` and face against the computer in a simple game of Rock Paper Scissors!

## Model Training Notes
- This model was trained utilizing a CNN for image classification utilizing a variety of Rock Paper Scissors Datasets. The Kaggle/Jupyter Notebook can be found [here](https://github.com/derzz/RPS-Keras).
- Overall, the model was trained several times and gained 92.73% accuracy on the test data:
![model accuracy](https://github.com/user-attachments/assets/55654a8b-5a0a-433a-b217-e8bc6d1a8c44)

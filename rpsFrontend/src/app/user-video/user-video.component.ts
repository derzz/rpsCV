import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-user-video',
  standalone: true,
  imports: [],
  templateUrl: './user-video.component.html',
  styleUrl: './user-video.component.scss'
})
export class UserVideoComponent implements OnInit{

  constructor(private http: HttpClient) {}

  baseUrl: string = "http://localhost:8000" // TODO Need to change and store as a secrets file

  title = 'rpsFrontend';
  constraints = {
    audio: false,
    video: true,
  };
  video!: HTMLVideoElement;
  canvas!: HTMLCanvasElement;
  videoTracks: any;
  errorMsg: string = "";
  responseData?: any;
  robotResponse = ""
  winner = ""

  videoSuccess(stream: MediaStream) {
    const video = document.querySelector('video');
    this.videoTracks = stream.getVideoTracks();
    console.log('Got stream with constraints:', this.constraints);
    console.log(`Using video device: ${this.videoTracks[0].label}`);
    video!.srcObject = stream;
  }

  videoError(error: any) {
    console.log(error);
  }


  private decision() {
    if (!this.responseData || !this.responseData.rps) {
      this.winner = "No valid response from user.";
      return;
    }

    const userResponse = this.responseData.rps;
    const robotResponse = this.robotResponse;

    if (userResponse === robotResponse) {
      this.winner = "It's a tie!";
    } else if (
      (userResponse === "Rock" && robotResponse === "Scissors") ||
      (userResponse === "Paper" && robotResponse === "Rock") ||
      (userResponse === "Scissors" && robotResponse === "Paper")
    ) {
      this.winner = "User wins!";
    } else {
      this.winner = "Robot wins!";
    }
  }

  takePicture() {
    const context = this.canvas.getContext('2d');
    this.errorMsg = ""
    this.responseData = null
    if (context) {
      this.canvas.width = this.video.videoWidth;
      this.canvas.height = this.video.videoHeight;
      context.drawImage(
        this.video,
        0,
        0,
        this.video.videoWidth,
        this.video.videoHeight
      );
      context.fill();
      console.log('taken picture!');
	  const data = this.canvas.toDataURL("image/png")
	  console.log(data)

      let tempRobot:number = Math.round(Math.random() * 3)
      this.robotResponse = tempRobot == 0 ? "Rock" : tempRobot == 1 ? "Paper" : "Scissors"
      this.http.post(this.baseUrl + '/fileURL/', {url: data}).subscribe(
        response =>{
            this.responseData = response;
            this.decision()
        },
        (error: HttpErrorResponse) =>{
            console.log("recieved error")
            if (error.status == 400){
                this.errorMsg = "Unable to detect a hand."
                console.log("400")
            }
            else{
                this.errorMsg = "Error. Please see console logs."
                console.log(error)
            }
        }
      );
    }
  }

  async ngOnInit() {
    this.video = document.getElementById('video') as HTMLVideoElement;
    this.canvas = document.getElementById('canvas') as HTMLCanvasElement;
    try {
      const stream: MediaStream = await navigator.mediaDevices.getUserMedia(
        this.constraints
      );
      this.videoSuccess(stream);
    } catch (e) {
      this.videoError(e);
    }
  }
}

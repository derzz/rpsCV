import { Component, OnInit, ViewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BarChartComponent } from '../bar-chart/bar-chart.component';

@Component({
  selector: 'app-user-video',
  standalone: true,
  imports: [BarChartComponent],
  templateUrl: './user-video.component.html',
  styleUrl: './user-video.component.scss',
})
export class UserVideoComponent implements OnInit {
  constructor(private http: HttpClient) {}

  baseUrl: string = 'http://localhost:8000'; // TODO Need to change and store as a secrets file

  title = 'rpsFrontend';
  constraints = {
    audio: false,
    video: true,
  };
  video!: HTMLVideoElement;
  canvas!: HTMLCanvasElement;
  videoTracks: any;
  errorMsg: string = '';
  responseData?: any;
  robotResponse = '';
  responseEmoji = '';
  robotEmoji = '';
  winner = 'Who will win?';
  robotScore = 0;
  humanScore = 0;
  rock = 0;
  paper = 0;
  scissors = 0;


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

  private emojiSelector(response: string): string {
    if (response === 'Rock') {
      return '✊';
    } else if (response === 'Paper') {
      return '✋';
    } else {
      return '✌️';
    }
  }

  private decision() {
    if (!this.responseData || !this.responseData.rps) {
      this.winner = 'No valid response from user.';
      return;
    }
    this.responseEmoji = this.emojiSelector(this.responseData.rps);
    this.robotEmoji = this.emojiSelector(this.robotResponse);
    const userResponse = this.responseData.rps;
    const robotResponse = this.robotResponse;

    if (userResponse === robotResponse){
      this.winner = "It's a tie!";
    } else if (
      (userResponse === 'Rock' && robotResponse === 'Scissors') ||
      (userResponse === 'Paper' && robotResponse === 'Rock') ||
      (userResponse === 'Scissors' && robotResponse === 'Paper')
    ) {
      this.winner = 'User wins!';
      this.humanScore += 1;
    } else {
      this.winner = 'Robot wins!';
      this.robotScore += 1;
    }

    this.rock = this.responseData.rock;
    this.paper = this.responseData.paper;
    this.scissors = this.responseData.scissors;
    console.log("decision finished")
  }

  takePicture() {
    const context = this.canvas.getContext('2d');
    this.errorMsg = '';
    this.responseData = null;
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
      const data = this.canvas.toDataURL('image/png');
      console.log(data);

      let tempRobot: number = Math.round(Math.random() * 3);
      this.robotResponse =
        tempRobot == 0 ? 'Rock' : tempRobot == 1 ? 'Paper' : 'Scissors';
      this.http.post(this.baseUrl + '/fileURL/', { url: data }).subscribe(
        (response) => {
          this.responseData = response;
          this.decision();
        },
        (error: HttpErrorResponse) => {
          console.log('recieved error');
          if (error.status == 400) {
            this.errorMsg = 'Unable to detect a hand.';
            console.log('400');
          } else {
            this.errorMsg = 'Error. Please see console logs.';
            console.log(error);
          }
        }
      );
    }
  }

}

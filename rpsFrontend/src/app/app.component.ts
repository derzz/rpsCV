import {Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})

export class AppComponent implements OnInit{
  title = 'rpsFrontend';
  constraints ={
    audio : false,
    video: true
  };
  video!: HTMLVideoElement;
  canvas!: HTMLCanvasElement;

  videoSuccess(stream: MediaStream){
    const video = document.querySelector('video')
    const videoTracks = stream.getVideoTracks();
    console.log('Got stream with constraints:', this.constraints);
    console.log(`Using video device: ${videoTracks[0].label}`);
    video!.srcObject = stream;
  }

  videoError(error: any){
    console.log(error)
  }

  takePicture() {
    const context = this.canvas.getContext('2d');
    if (context) {
      this.canvas.width = this.video.videoWidth;
      this.canvas.height = this.video.videoHeight;
      context.drawImage(this.video, 0, 0, this.video.videoWidth, this.video.videoHeight);
      context.fill();
      console.log("taken picture!");
    }
  }


  async ngOnInit() {
    this.video = document.getElementById('video') as HTMLVideoElement;
    this.canvas = document.getElementById('canvas') as HTMLCanvasElement;
    try{
      const stream:MediaStream = await navigator.mediaDevices.getUserMedia(this.constraints)
      this.videoSuccess(stream)
    }
    catch(e){
      this.videoError(e);
    }
  }

}

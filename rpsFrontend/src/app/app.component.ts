import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { UserVideoComponent } from "./user-video/user-video.component";

// TODO Implement API request
// TODO Game Logic
// TODO Allow multiple camera sources

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, UserVideoComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})

export class AppComponent {
}

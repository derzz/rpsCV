import { Component, OnInit } from '@angular/core';
import {BaseChartDirective} from 'ng2-charts'
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';

@Component({
  selector: 'app-bar-chart',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './bar-chart.component.html',
  styleUrl: './bar-chart.component.scss',
})
export class BarChartComponent implements OnInit {
  // Chart configuration
  public barChartOptions: ChartOptions = {
    scales: {
        y: {
            beginAtZero: true,
            max: 1,
            min: 0
        }
    },
    plugins:{
        legend: {
            display: false,
        },
        title:{
            display: true,
            text: 'CV Probabilities',
        }
    }
  };
  public barChartLabels: string[] = ['✊', '✋', '✌️'];
  public barChartType: ChartType = 'bar';
  public barChartLegend = false;
  public barChartPlugins = [];
  public barChartData: ChartConfiguration['data'] = {
    labels: this.barChartLabels,
    datasets: [
      {
        data: [0.2, 0.6, 0.2],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  constructor() {}

  ngOnInit(): void {}
}

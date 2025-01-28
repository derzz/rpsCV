import { Component, OnInit, Input, SimpleChanges, OnChanges, ViewChild } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';

@Component({
  selector: 'app-bar-chart',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './bar-chart.component.html',
  styleUrl: './bar-chart.component.scss',
})
export class BarChartComponent implements OnInit, OnChanges {
  @Input() rock: number = 0.2;
  @Input() paper: number = 0;
@Input() scissors: number = 0;
  @ViewChild(BaseChartDirective) chart: BaseChartDirective;

  // Chart configuration
  public barChartOptions: ChartOptions = {
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        min: 0,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'CV Probabilities',
      },
    },
  };
  public barChartLabels: string[] = ['✊', '✋', '✌️'];
  public barChartType: ChartType = 'bar';
  public barChartLegend = false;
  public barChartPlugins = [];
  public barChartData: ChartConfiguration['data'] = {
    labels: this.barChartLabels,
    datasets: [
      {
        data: [this.rock, this.paper, this.scissors],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  constructor() {}

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['rock'] || changes['paper'] || changes['scissors']) {
      this.updateChartData();
      this.updateChart();
    }
  }

  private updateChartData(): void {
    this.barChartData.datasets[0].data = [this.rock, this.paper, this.scissors];
  }

  private updateChart(): void {
    if (this.chart) {
      this.chart.chart?.update();
    }
  }
}

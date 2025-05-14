import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { NgChartsModule } from 'ng2-charts';
import { ChartConfiguration, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-predict-timeseries',
  standalone: true,
  imports: [CommonModule, HttpClientModule, NgChartsModule],
  templateUrl: './predict-timeseries.component.html',
})
export class PredictTimeseriesComponent implements OnInit {
  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [],
    datasets: [
      {
        data: [],
        label: 'Prévision (yhat)',
        borderColor: '#42a5f5',
        backgroundColor: 'rgba(66, 165, 245, 0.2)',
        fill: false,
        tension: 0.3,
        pointRadius: 3
      },
      {
        data: [],
        label: 'Borne Inférieure',
        borderColor: 'rgba(255,99,132,0.5)',
        borderDash: [5, 5],
        fill: false,
        tension: 0.3,
        pointRadius: 0
      },
      {
        data: [],
        label: 'Borne Supérieure',
        borderColor: 'rgba(255,206,86,0.5)',
        borderDash: [5, 5],
        fill: false,
        tension: 0.3,
        pointRadius: 0
      }
    ]
  };

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: {
        display: true
      }
    },
    scales: {
      x: {},
      y: {
        beginAtZero: false
      }
    }
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any>('http://localhost:5000/predict-timeseries?days=30')
      .subscribe({
        next: res => {
          const forecast = res.forecast;
          console.log('📈 Données forecast reçues :', forecast);

          if (forecast && forecast.length > 0) {
            this.lineChartData.labels = forecast.map((d: any) => d.ds);
            this.lineChartData.datasets[0].data = forecast.map((d: any) => d.yhat);
            this.lineChartData.datasets[1].data = forecast.map((d: any) => d.yhat_lower);
            this.lineChartData.datasets[2].data = forecast.map((d: any) => d.yhat_upper);
          } else {
            console.warn('⚠️ Aucune donnée reçue du backend.');
          }
        },
        error: err => {
          console.error('❌ Erreur API /predict-timeseries :', err);
        }
      });
  }
}

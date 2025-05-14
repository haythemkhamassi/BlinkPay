import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-predict-cluster',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './predict-cluster.component.html',
  styleUrls: ['./predict-cluster.component.css']
})
export class PredictClusterComponent {
  input = {
    Gender: '',
    Age: '',
    Annual_Income: '',
    Spending_Score__1_100: '',
    Work_Experience: '',
    Family_Size: ''
  };

  cluster: number | null = null;

  constructor(private http: HttpClient) {}

  sendPrediction() {
    this.http.post<any>('http://localhost:5000/predict-cluster', this.input)
      .subscribe({
        next: res => this.cluster = res.cluster,
        error: err => console.error('Erreur :', err)
      });
  }
}

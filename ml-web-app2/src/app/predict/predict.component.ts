import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';

// 🟦 Angular Material modules
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';

@Component({
  selector: 'app-predict',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDividerModule
  ],
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css']
})
export class PredictComponent {
 input = {
  Amortissement_Cumule: '', // au lieu de 0
  Cout_de_Maintenance: '',
  Investissement_dans_les_Actifs: ''
};


  prediction: number | null = null;

  constructor(private http: HttpClient) {}

  sendPrediction() {
    this.http.post<any>('http://localhost:5000/predict', this.input)
      .subscribe({
        next: res => this.prediction = res.prediction,
        error: err => console.error('Erreur de prédiction', err)
      });
  }
}

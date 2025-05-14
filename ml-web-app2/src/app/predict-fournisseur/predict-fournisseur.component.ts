import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-predict-fournisseur',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './predict-fournisseur.component.html',
  styleUrls: ['./predict-fournisseur.component.css']
})
export class PredictFournisseurComponent {
  formData = {
    NbCommandes: "",
    MontantTotal: "",
    DelaiPaiement: "",
    TypePaiement: 'Carte'
  };

  prediction: number | null = null;

  constructor(private http: HttpClient) {}

  onSubmit() {
    const payload = {
      NbCommandes: this.formData.NbCommandes,
      MontantTotal: this.formData.MontantTotal,
      DelaiPaiement: this.formData.DelaiPaiement,
      TypePaiement_Carte: this.formData.TypePaiement === 'Carte' ? 1 : 0,
      TypePaiement_Espèces: this.formData.TypePaiement === 'Espèces' ? 1 : 0,
      TypePaiement_Virement: this.formData.TypePaiement === 'Virement' ? 1 : 0
    };

    this.http.post<any>('http://localhost:5000/predict-fournisseur', payload)
      .subscribe({
        next: res => this.prediction = res.fiabilite,
        error: err => {
          console.error(err);
          this.prediction = null;
        }
      });
  }
}

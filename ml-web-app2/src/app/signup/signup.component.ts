import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router'; 
@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  styleUrls: ['./signup.component.css'],
  templateUrl: './signup.component.html'
})
export class SignupComponent {
  email = '';
  password = '';
  role = 'Manager';
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  signup() {
    const success = this.auth.signup(this.email, this.password, this.role);
    if (success) {
      if (this.role === 'Manager') this.router.navigate(['/regression']);
      else if (this.role === 'CFO') this.router.navigate(['/dashboard']);
    } else {
      this.error = 'Un compte avec cet email existe déjà';
    }
  }
}

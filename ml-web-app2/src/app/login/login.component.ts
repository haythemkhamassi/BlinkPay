import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router'; // ✅ IMPORT THIS

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  login() {
    const success = this.auth.login(this.email, this.password);
    if (success) {
      const role = this.auth.getRole();
      if (role === 'Manager') this.router.navigate(['/regression']);
else if (role === 'CFO') this.router.navigate(['/dashboard/analysis']);
    } else {
      this.error = 'Email ou mot de passe incorrect';
    }
  }
}

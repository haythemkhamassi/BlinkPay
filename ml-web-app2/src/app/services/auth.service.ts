import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private users: any[] = [];
  private currentUser: any = null;

  constructor() {
    // Charger les utilisateurs sauvegardés depuis localStorage
    const savedUsers = localStorage.getItem('users');
    if (savedUsers) {
      this.users = JSON.parse(savedUsers);
    } else {
      // utilisateurs initiaux si rien en localStorage
      this.users = [
        { email: 'manager@test.com', password: '123456', role: 'Manager' },
        { email: 'cfo@test.com', password: '123456', role: 'CFO' }
      ];
      localStorage.setItem('users', JSON.stringify(this.users));
    }

    // Charger l'utilisateur connecté
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      this.currentUser = JSON.parse(savedUser);
    }
  }

  login(email: string, password: string): boolean {
    const user = this.users.find(u => u.email === email && u.password === password);
    if (user) {
      this.currentUser = user;
      localStorage.setItem('user', JSON.stringify(user));
      return true;
    }
    return false;
  }

  signup(email: string, password: string, role: string): boolean {
    const exists = this.users.find(u => u.email === email);
    if (exists) return false;

    const newUser = { email, password, role };
    this.users.push(newUser);
    localStorage.setItem('users', JSON.stringify(this.users));

    this.currentUser = newUser;
    localStorage.setItem('user', JSON.stringify(newUser));
    return true;
  }

  logout() {
    this.currentUser = null;
    localStorage.removeItem('user');
  }

  getCurrentUser() {
    if (!this.currentUser) {
      try {
        const user = localStorage.getItem('user');
        if (user) {
          this.currentUser = JSON.parse(user);
        }
      } catch {
        this.logout();
      }
    }
    return this.currentUser;
  }

  getRole() {
    return this.getCurrentUser()?.role || null;
  }
}

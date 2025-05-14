import { Injectable } from '@angular/core';
import { CanActivateFn, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const expectedRoles = route.data['roles'] as string[];
    const user = this.auth.getCurrentUser();

    if (!user || !expectedRoles.includes(user.role)) {
      this.router.navigate(['/login']);
      return false;
    }

    return true;
  }
}

import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { MainLayoutComponent } from './layout/main-layout.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'signup',
    loadComponent: () => import('./signup/signup.component').then(m => m.SignupComponent)
  },
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      {
        path: 'regression',
        loadComponent: () => import('./predict/predict.component').then(m => m.PredictComponent),
        canActivate: [RoleGuard],
        data: { roles: ['Manager'] }
      },
      {
        path: 'cluster',
        loadComponent: () => import('./predict-cluster/predict-cluster.component').then(m => m.PredictClusterComponent),
        canActivate: [RoleGuard],
        data: { roles: ['CFO'] }
      },
      {
        path: 'timeseries',
        loadComponent: () => import('./predict-timeseries/predict-timeseries.component').then(m => m.PredictTimeseriesComponent),
        canActivate: [RoleGuard],
        data: { roles: ['Manager'] }
      },
      {
        path: 'predict-fournisseur',
        loadComponent: () => import('./predict-fournisseur/predict-fournisseur.component').then(m => m.PredictFournisseurComponent),
        canActivate: [RoleGuard],
        data: { roles: ['CFO'] }
      },

      // ✅ Dashboard pages (Grouped under 'dashboard')
      {
        path: 'dashboard',
        children: [
          {
            path: '',
            redirectTo: 'overview',
            pathMatch: 'full'
          },
          {
            path: 'overview',
            loadComponent: () => import('./powerbi/powerbi.component').then(m => m.PowerbiComponent),
            canActivate: [RoleGuard],
            data: { roles: ['Manager'] }
          },
          {
            path: 'analysis',
            loadComponent: () => import('./powerbi/powerbi.component').then(m => m.PowerbiComponent),
            canActivate: [RoleGuard],
            data: { roles: ['CFO'] }
          },
          {
            path: 'sales',
            loadComponent: () => import('./powerbi/powerbi.component').then(m => m.PowerbiComponent),
            canActivate: [RoleGuard],
            data: { roles: ['Manager'] }
          },
          {
            path: 'product',
            loadComponent: () => import('./powerbi/powerbi.component').then(m => m.PowerbiComponent),
            canActivate: [RoleGuard],
            data: { roles: ['CFO'] }
          }
        ]
      }
    ]
  },

  // Optional: Catch-all route (goes last)
  {
    path: '**',
    redirectTo: 'login'
  }
];

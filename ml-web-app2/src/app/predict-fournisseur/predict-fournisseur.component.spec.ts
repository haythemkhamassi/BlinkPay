import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictFournisseurComponent } from './predict-fournisseur.component';

describe('PredictFournisseurComponent', () => {
  let component: PredictFournisseurComponent;
  let fixture: ComponentFixture<PredictFournisseurComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictFournisseurComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictFournisseurComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

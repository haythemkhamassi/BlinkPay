import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictClusterComponent } from './predict-cluster.component';

describe('PredictClusterComponent', () => {
  let component: PredictClusterComponent;
  let fixture: ComponentFixture<PredictClusterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictClusterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictClusterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

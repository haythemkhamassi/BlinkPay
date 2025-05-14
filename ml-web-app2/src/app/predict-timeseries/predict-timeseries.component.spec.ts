import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictTimeseriesComponent } from './predict-timeseries.component';

describe('PredictTimeseriesComponent', () => {
  let component: PredictTimeseriesComponent;
  let fixture: ComponentFixture<PredictTimeseriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictTimeseriesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictTimeseriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsBigComponent } from './news-big.component';

describe('NewsBigComponent', () => {
  let component: NewsBigComponent;
  let fixture: ComponentFixture<NewsBigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewsBigComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewsBigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

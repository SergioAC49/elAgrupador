import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsMediumComponent } from './news-medium.component';

describe('NewsMediumComponent', () => {
  let component: NewsMediumComponent;
  let fixture: ComponentFixture<NewsMediumComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewsMediumComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewsMediumComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

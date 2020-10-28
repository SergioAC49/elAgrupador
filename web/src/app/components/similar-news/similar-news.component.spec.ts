import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimilarNewsComponent } from './similar-news.component';

describe('SimilarNewsComponent', () => {
  let component: SimilarNewsComponent;
  let fixture: ComponentFixture<SimilarNewsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SimilarNewsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SimilarNewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { YamlreadComponent } from './yamlread.component';

describe('YamlreadComponent', () => {
  let component: YamlreadComponent;
  let fixture: ComponentFixture<YamlreadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ YamlreadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(YamlreadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

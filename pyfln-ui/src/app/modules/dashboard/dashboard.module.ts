import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IndexComponent } from './index/index.component';
import { YamlreadComponent } from './yamlread/yamlread.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [IndexComponent, YamlreadComponent]
})
export class DashboardModule { }

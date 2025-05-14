import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-powerbi',
  templateUrl: './powerbi.component.html',
  styleUrls: ['./powerbi.component.css']
})
export class PowerbiComponent {
  iframeUrl: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) {
    this.iframeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
      'https://app.powerbi.com/reportEmbed?reportId=3998ed7a-3fc0-43fd-a147-734167a88e93&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730'
    );
  }
}

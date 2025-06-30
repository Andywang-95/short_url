import Alpine from 'alpinejs';
import htmx from 'htmx.org';
import { copyShortUrl } from './copyShortUrl.js';

window.Alpine = Alpine

Alpine.data('copyShortUrl', copyShortUrl);
Alpine.start()

/* Polish: keep the current nav item in view on narrow screens; fade the strip edges only where more items exist. */
(function(){var n=document.querySelector('header nav');if(!n)return;
function edge(){var s=n.scrollLeft<=2,e=n.scrollLeft+n.clientWidth>=n.scrollWidth-2;n.classList.toggle('nm-start',s);n.classList.toggle('nm-end',e);n.classList.toggle('nm-mid',!s&&!e)}
var c=n.querySelector('[aria-current]');if(c&&n.scrollWidth>n.clientWidth){var l=c.offsetLeft-(n.clientWidth-c.offsetWidth)/2;n.scrollLeft=Math.max(0,l)}
edge();n.addEventListener('scroll',edge,{passive:true});addEventListener('resize',edge)})();

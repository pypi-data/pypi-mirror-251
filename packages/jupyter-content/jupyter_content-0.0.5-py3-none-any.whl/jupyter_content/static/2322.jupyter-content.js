"use strict";(self.webpackChunk_datalayer_jupyter_content=self.webpackChunk_datalayer_jupyter_content||[]).push([[2322],{42322:(e,t,r)=>{function o(e){var t,r,o=(e={...q,...e}).inline,i=e.tokenHooks,a=e.documentTypes||{},n=e.mediaTypes||{},l=e.mediaFeatures||{},s=e.mediaValueKeywords||{},c=e.propertyKeywords||{},d=e.nonStandardPropertyKeywords||{},p=e.fontProperties||{},u=e.counterDescriptors||{},m=e.colorKeywords||{},g=e.valueKeywords||{},h=e.allowNested,b=e.lineComment,f=!0===e.supportsAtComponent,k=!1!==e.highlightNonStandardPropertyKeywords;function y(e,r){return t=r,e}function w(e,t){var r=e.next();if(i[r]){var o=i[r](e,t);if(!1!==o)return o}return"@"==r?(e.eatWhile(/[\w\\\-]/),y("def",e.current())):"="==r||("~"==r||"|"==r)&&e.eat("=")?y(null,"compare"):'"'==r||"'"==r?(t.tokenize=v(r),t.tokenize(e,t)):"#"==r?(e.eatWhile(/[\w\\\-]/),y("atom","hash")):"!"==r?(e.match(/^\s*\w*/),y("keyword","important")):/\d/.test(r)||"."==r&&e.eat(/\d/)?(e.eatWhile(/[\w.%]/),y("number","unit")):"-"!==r?/[,+>*\/]/.test(r)?y(null,"select-op"):"."==r&&e.match(/^-?[_a-z][_a-z0-9-]*/i)?y("qualifier","qualifier"):/[:;{}\[\]\(\)]/.test(r)?y(null,r):e.match(/^[\w-.]+(?=\()/)?(/^(url(-prefix)?|domain|regexp)$/i.test(e.current())&&(t.tokenize=x),y("variableName.function","variable")):/[\w\\\-]/.test(r)?(e.eatWhile(/[\w\\\-]/),y("property","word")):y(null,null):/[\d.]/.test(e.peek())?(e.eatWhile(/[\w.%]/),y("number","unit")):e.match(/^-[\w\\\-]*/)?(e.eatWhile(/[\w\\\-]/),e.match(/^\s*:/,!1)?y("def","variable-definition"):y("variableName","variable")):e.match(/^\w+-/)?y("meta","meta"):void 0}function v(e){return function(t,r){for(var o,i=!1;null!=(o=t.next());){if(o==e&&!i){")"==e&&t.backUp(1);break}i=!i&&"\\"==o}return(o==e||!i&&")"!=e)&&(r.tokenize=null),y("string","string")}}function x(e,t){return e.next(),e.match(/^\s*[\"\')]/,!1)?t.tokenize=null:t.tokenize=v(")"),y(null,"(")}function z(e,t,r){this.type=e,this.indent=t,this.prev=r}function P(e,t,r,o){return e.context=new z(r,t.indentation()+(!1===o?0:t.indentUnit),e.context),r}function K(e){return e.context.prev&&(e.context=e.context.prev),e.context.type}function _(e,t,r){return O[r.context.type](e,t,r)}function B(e,t,r,o){for(var i=o||1;i>0;i--)r.context=r.context.prev;return _(e,t,r)}function C(e){var t=e.current().toLowerCase();r=g.hasOwnProperty(t)?"atom":m.hasOwnProperty(t)?"keyword":"variable"}var O={top:function(e,t,o){if("{"==e)return P(o,t,"block");if("}"==e&&o.context.prev)return K(o);if(f&&/@component/i.test(e))return P(o,t,"atComponentBlock");if(/^@(-moz-)?document$/i.test(e))return P(o,t,"documentTypes");if(/^@(media|supports|(-moz-)?document|import)$/i.test(e))return P(o,t,"atBlock");if(/^@(font-face|counter-style)/i.test(e))return o.stateArg=e,"restricted_atBlock_before";if(/^@(-(moz|ms|o|webkit)-)?keyframes$/i.test(e))return"keyframes";if(e&&"@"==e.charAt(0))return P(o,t,"at");if("hash"==e)r="builtin";else if("word"==e)r="tag";else{if("variable-definition"==e)return"maybeprop";if("interpolation"==e)return P(o,t,"interpolation");if(":"==e)return"pseudo";if(h&&"("==e)return P(o,t,"parens")}return o.context.type},block:function(e,t,o){if("word"==e){var i=t.current().toLowerCase();return c.hasOwnProperty(i)?(r="property","maybeprop"):d.hasOwnProperty(i)?(r=k?"string.special":"property","maybeprop"):h?(r=t.match(/^\s*:(?:\s|$)/,!1)?"property":"tag","block"):(r="error","maybeprop")}return"meta"==e?"block":h||"hash"!=e&&"qualifier"!=e?O.top(e,t,o):(r="error","block")},maybeprop:function(e,t,r){return":"==e?P(r,t,"prop"):_(e,t,r)},prop:function(e,t,o){if(";"==e)return K(o);if("{"==e&&h)return P(o,t,"propBlock");if("}"==e||"{"==e)return B(e,t,o);if("("==e)return P(o,t,"parens");if("hash"!=e||/^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/.test(t.current())){if("word"==e)C(t);else if("interpolation"==e)return P(o,t,"interpolation")}else r="error";return"prop"},propBlock:function(e,t,o){return"}"==e?K(o):"word"==e?(r="property","maybeprop"):o.context.type},parens:function(e,t,r){return"{"==e||"}"==e?B(e,t,r):")"==e?K(r):"("==e?P(r,t,"parens"):"interpolation"==e?P(r,t,"interpolation"):("word"==e&&C(t),"parens")},pseudo:function(e,t,o){return"meta"==e?"pseudo":"word"==e?(r="variableName.constant",o.context.type):_(e,t,o)},documentTypes:function(e,t,o){return"word"==e&&a.hasOwnProperty(t.current())?(r="tag",o.context.type):O.atBlock(e,t,o)},atBlock:function(e,t,o){if("("==e)return P(o,t,"atBlock_parens");if("}"==e||";"==e)return B(e,t,o);if("{"==e)return K(o)&&P(o,t,h?"block":"top");if("interpolation"==e)return P(o,t,"interpolation");if("word"==e){var i=t.current().toLowerCase();r="only"==i||"not"==i||"and"==i||"or"==i?"keyword":n.hasOwnProperty(i)?"attribute":l.hasOwnProperty(i)?"property":s.hasOwnProperty(i)?"keyword":c.hasOwnProperty(i)?"property":d.hasOwnProperty(i)?k?"string.special":"property":g.hasOwnProperty(i)?"atom":m.hasOwnProperty(i)?"keyword":"error"}return o.context.type},atComponentBlock:function(e,t,o){return"}"==e?B(e,t,o):"{"==e?K(o)&&P(o,t,h?"block":"top",!1):("word"==e&&(r="error"),o.context.type)},atBlock_parens:function(e,t,r){return")"==e?K(r):"{"==e||"}"==e?B(e,t,r,2):O.atBlock(e,t,r)},restricted_atBlock_before:function(e,t,o){return"{"==e?P(o,t,"restricted_atBlock"):"word"==e&&"@counter-style"==o.stateArg?(r="variable","restricted_atBlock_before"):_(e,t,o)},restricted_atBlock:function(e,t,o){return"}"==e?(o.stateArg=null,K(o)):"word"==e?(r="@font-face"==o.stateArg&&!p.hasOwnProperty(t.current().toLowerCase())||"@counter-style"==o.stateArg&&!u.hasOwnProperty(t.current().toLowerCase())?"error":"property","maybeprop"):"restricted_atBlock"},keyframes:function(e,t,o){return"word"==e?(r="variable","keyframes"):"{"==e?P(o,t,"top"):_(e,t,o)},at:function(e,t,o){return";"==e?K(o):"{"==e||"}"==e?B(e,t,o):("word"==e?r="tag":"hash"==e&&(r="builtin"),"at")},interpolation:function(e,t,o){return"}"==e?K(o):"{"==e||";"==e?B(e,t,o):("word"==e?r="variable":"variable"!=e&&"("!=e&&")"!=e&&(r="error"),"interpolation")}};return{name:e.name,startState:function(){return{tokenize:null,state:o?"block":"top",stateArg:null,context:new z(o?"block":"top",0,null)}},token:function(e,o){if(!o.tokenize&&e.eatSpace())return null;var i=(o.tokenize||w)(e,o);return i&&"object"==typeof i&&(t=i[1],i=i[0]),r=i,"comment"!=t&&(o.state=O[o.state](t,e,o)),r},indent:function(e,t,r){var o=e.context,i=t&&t.charAt(0),a=o.indent;return"prop"!=o.type||"}"!=i&&")"!=i||(o=o.prev),o.prev&&("}"!=i||"block"!=o.type&&"top"!=o.type&&"interpolation"!=o.type&&"restricted_atBlock"!=o.type?(")"!=i||"parens"!=o.type&&"atBlock_parens"!=o.type)&&("{"!=i||"at"!=o.type&&"atBlock"!=o.type)||(a=Math.max(0,o.indent-r.unit)):a=(o=o.prev).indent),a},languageData:{indentOnInput:/^\s*\}$/,commentTokens:{line:b,block:{open:"/*",close:"*/"}},autocomplete:j}}}function i(e){for(var t={},r=0;r<e.length;++r)t[e[r].toLowerCase()]=!0;return t}r.r(t),r.d(t,{css:()=>K,gss:()=>O,keywords:()=>P,less:()=>C,mkCSS:()=>o,sCSS:()=>B});var a=["domain","regexp","url","url-prefix"],n=i(a),l=["all","aural","braille","handheld","print","projection","screen","tty","tv","embossed"],s=i(l),c=["width","min-width","max-width","height","min-height","max-height","device-width","min-device-width","max-device-width","device-height","min-device-height","max-device-height","aspect-ratio","min-aspect-ratio","max-aspect-ratio","device-aspect-ratio","min-device-aspect-ratio","max-device-aspect-ratio","color","min-color","max-color","color-index","min-color-index","max-color-index","monochrome","min-monochrome","max-monochrome","resolution","min-resolution","max-resolution","scan","grid","orientation","device-pixel-ratio","min-device-pixel-ratio","max-device-pixel-ratio","pointer","any-pointer","hover","any-hover","prefers-color-scheme","dynamic-range","video-dynamic-range"],d=i(c),p=["landscape","portrait","none","coarse","fine","on-demand","hover","interlace","progressive","dark","light","standard","high"],u=i(p),m=["align-content","align-items","align-self","alignment-adjust","alignment-baseline","all","anchor-point","animation","animation-delay","animation-direction","animation-duration","animation-fill-mode","animation-iteration-count","animation-name","animation-play-state","animation-timing-function","appearance","azimuth","backdrop-filter","backface-visibility","background","background-attachment","background-blend-mode","background-clip","background-color","background-image","background-origin","background-position","background-position-x","background-position-y","background-repeat","background-size","baseline-shift","binding","bleed","block-size","bookmark-label","bookmark-level","bookmark-state","bookmark-target","border","border-bottom","border-bottom-color","border-bottom-left-radius","border-bottom-right-radius","border-bottom-style","border-bottom-width","border-collapse","border-color","border-image","border-image-outset","border-image-repeat","border-image-slice","border-image-source","border-image-width","border-left","border-left-color","border-left-style","border-left-width","border-radius","border-right","border-right-color","border-right-style","border-right-width","border-spacing","border-style","border-top","border-top-color","border-top-left-radius","border-top-right-radius","border-top-style","border-top-width","border-width","bottom","box-decoration-break","box-shadow","box-sizing","break-after","break-before","break-inside","caption-side","caret-color","clear","clip","color","color-profile","column-count","column-fill","column-gap","column-rule","column-rule-color","column-rule-style","column-rule-width","column-span","column-width","columns","contain","content","counter-increment","counter-reset","crop","cue","cue-after","cue-before","cursor","direction","display","dominant-baseline","drop-initial-after-adjust","drop-initial-after-align","drop-initial-before-adjust","drop-initial-before-align","drop-initial-size","drop-initial-value","elevation","empty-cells","fit","fit-content","fit-position","flex","flex-basis","flex-direction","flex-flow","flex-grow","flex-shrink","flex-wrap","float","float-offset","flow-from","flow-into","font","font-family","font-feature-settings","font-kerning","font-language-override","font-optical-sizing","font-size","font-size-adjust","font-stretch","font-style","font-synthesis","font-variant","font-variant-alternates","font-variant-caps","font-variant-east-asian","font-variant-ligatures","font-variant-numeric","font-variant-position","font-variation-settings","font-weight","gap","grid","grid-area","grid-auto-columns","grid-auto-flow","grid-auto-rows","grid-column","grid-column-end","grid-column-gap","grid-column-start","grid-gap","grid-row","grid-row-end","grid-row-gap","grid-row-start","grid-template","grid-template-areas","grid-template-columns","grid-template-rows","hanging-punctuation","height","hyphens","icon","image-orientation","image-rendering","image-resolution","inline-box-align","inset","inset-block","inset-block-end","inset-block-start","inset-inline","inset-inline-end","inset-inline-start","isolation","justify-content","justify-items","justify-self","left","letter-spacing","line-break","line-height","line-height-step","line-stacking","line-stacking-ruby","line-stacking-shift","line-stacking-strategy","list-style","list-style-image","list-style-position","list-style-type","margin","margin-bottom","margin-left","margin-right","margin-top","marks","marquee-direction","marquee-loop","marquee-play-count","marquee-speed","marquee-style","mask-clip","mask-composite","mask-image","mask-mode","mask-origin","mask-position","mask-repeat","mask-size","mask-type","max-block-size","max-height","max-inline-size","max-width","min-block-size","min-height","min-inline-size","min-width","mix-blend-mode","move-to","nav-down","nav-index","nav-left","nav-right","nav-up","object-fit","object-position","offset","offset-anchor","offset-distance","offset-path","offset-position","offset-rotate","opacity","order","orphans","outline","outline-color","outline-offset","outline-style","outline-width","overflow","overflow-style","overflow-wrap","overflow-x","overflow-y","padding","padding-bottom","padding-left","padding-right","padding-top","page","page-break-after","page-break-before","page-break-inside","page-policy","pause","pause-after","pause-before","perspective","perspective-origin","pitch","pitch-range","place-content","place-items","place-self","play-during","position","presentation-level","punctuation-trim","quotes","region-break-after","region-break-before","region-break-inside","region-fragment","rendering-intent","resize","rest","rest-after","rest-before","richness","right","rotate","rotation","rotation-point","row-gap","ruby-align","ruby-overhang","ruby-position","ruby-span","scale","scroll-behavior","scroll-margin","scroll-margin-block","scroll-margin-block-end","scroll-margin-block-start","scroll-margin-bottom","scroll-margin-inline","scroll-margin-inline-end","scroll-margin-inline-start","scroll-margin-left","scroll-margin-right","scroll-margin-top","scroll-padding","scroll-padding-block","scroll-padding-block-end","scroll-padding-block-start","scroll-padding-bottom","scroll-padding-inline","scroll-padding-inline-end","scroll-padding-inline-start","scroll-padding-left","scroll-padding-right","scroll-padding-top","scroll-snap-align","scroll-snap-type","shape-image-threshold","shape-inside","shape-margin","shape-outside","size","speak","speak-as","speak-header","speak-numeral","speak-punctuation","speech-rate","stress","string-set","tab-size","table-layout","target","target-name","target-new","target-position","text-align","text-align-last","text-combine-upright","text-decoration","text-decoration-color","text-decoration-line","text-decoration-skip","text-decoration-skip-ink","text-decoration-style","text-emphasis","text-emphasis-color","text-emphasis-position","text-emphasis-style","text-height","text-indent","text-justify","text-orientation","text-outline","text-overflow","text-rendering","text-shadow","text-size-adjust","text-space-collapse","text-transform","text-underline-position","text-wrap","top","touch-action","transform","transform-origin","transform-style","transition","transition-delay","transition-duration","transition-property","transition-timing-function","translate","unicode-bidi","user-select","vertical-align","visibility","voice-balance","voice-duration","voice-family","voice-pitch","voice-range","voice-rate","voice-stress","voice-volume","volume","white-space","widows","width","will-change","word-break","word-spacing","word-wrap","writing-mode","z-index","clip-path","clip-rule","mask","enable-background","filter","flood-color","flood-opacity","lighting-color","stop-color","stop-opacity","pointer-events","color-interpolation","color-interpolation-filters","color-rendering","fill","fill-opacity","fill-rule","image-rendering","marker","marker-end","marker-mid","marker-start","paint-order","shape-rendering","stroke","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke-width","text-rendering","baseline-shift","dominant-baseline","glyph-orientation-horizontal","glyph-orientation-vertical","text-anchor","writing-mode"],g=i(m),h=["accent-color","aspect-ratio","border-block","border-block-color","border-block-end","border-block-end-color","border-block-end-style","border-block-end-width","border-block-start","border-block-start-color","border-block-start-style","border-block-start-width","border-block-style","border-block-width","border-inline","border-inline-color","border-inline-end","border-inline-end-color","border-inline-end-style","border-inline-end-width","border-inline-start","border-inline-start-color","border-inline-start-style","border-inline-start-width","border-inline-style","border-inline-width","content-visibility","margin-block","margin-block-end","margin-block-start","margin-inline","margin-inline-end","margin-inline-start","overflow-anchor","overscroll-behavior","padding-block","padding-block-end","padding-block-start","padding-inline","padding-inline-end","padding-inline-start","scroll-snap-stop","scrollbar-3d-light-color","scrollbar-arrow-color","scrollbar-base-color","scrollbar-dark-shadow-color","scrollbar-face-color","scrollbar-highlight-color","scrollbar-shadow-color","scrollbar-track-color","searchfield-cancel-button","searchfield-decoration","searchfield-results-button","searchfield-results-decoration","shape-inside","zoom"],b=i(h),f=["font-display","font-family","src","unicode-range","font-variant","font-feature-settings","font-stretch","font-weight","font-style"],k=i(f),y=i(["additive-symbols","fallback","negative","pad","prefix","range","speak-as","suffix","symbols","system"]),w=["aliceblue","antiquewhite","aqua","aquamarine","azure","beige","bisque","black","blanchedalmond","blue","blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate","coral","cornflowerblue","cornsilk","crimson","cyan","darkblue","darkcyan","darkgoldenrod","darkgray","darkgreen","darkgrey","darkkhaki","darkmagenta","darkolivegreen","darkorange","darkorchid","darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkslategrey","darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue","firebrick","floralwhite","forestgreen","fuchsia","gainsboro","ghostwhite","gold","goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo","ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral","lightcyan","lightgoldenrodyellow","lightgray","lightgreen","lightgrey","lightpink","lightsalmon","lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow","lime","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid","mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","mediumvioletred","midnightblue","mintcream","mistyrose","moccasin","navajowhite","navy","oldlace","olive","olivedrab","orange","orangered","orchid","palegoldenrod","palegreen","paleturquoise","palevioletred","papayawhip","peachpuff","peru","pink","plum","powderblue","purple","rebeccapurple","red","rosybrown","royalblue","saddlebrown","salmon","sandybrown","seagreen","seashell","sienna","silver","skyblue","slateblue","slategray","slategrey","snow","springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white","whitesmoke","yellow","yellowgreen"],v=i(w),x=["above","absolute","activeborder","additive","activecaption","afar","after-white-space","ahead","alias","all","all-scroll","alphabetic","alternate","always","amharic","amharic-abegede","antialiased","appworkspace","arabic-indic","armenian","asterisks","attr","auto","auto-flow","avoid","avoid-column","avoid-page","avoid-region","axis-pan","background","backwards","baseline","below","bidi-override","binary","bengali","blink","block","block-axis","blur","bold","bolder","border","border-box","both","bottom","break","break-all","break-word","brightness","bullets","button","buttonface","buttonhighlight","buttonshadow","buttontext","calc","cambodian","capitalize","caps-lock-indicator","caption","captiontext","caret","cell","center","checkbox","circle","cjk-decimal","cjk-earthly-branch","cjk-heavenly-stem","cjk-ideographic","clear","clip","close-quote","col-resize","collapse","color","color-burn","color-dodge","column","column-reverse","compact","condensed","conic-gradient","contain","content","contents","content-box","context-menu","continuous","contrast","copy","counter","counters","cover","crop","cross","crosshair","cubic-bezier","currentcolor","cursive","cyclic","darken","dashed","decimal","decimal-leading-zero","default","default-button","dense","destination-atop","destination-in","destination-out","destination-over","devanagari","difference","disc","discard","disclosure-closed","disclosure-open","document","dot-dash","dot-dot-dash","dotted","double","down","drop-shadow","e-resize","ease","ease-in","ease-in-out","ease-out","element","ellipse","ellipsis","embed","end","ethiopic","ethiopic-abegede","ethiopic-abegede-am-et","ethiopic-abegede-gez","ethiopic-abegede-ti-er","ethiopic-abegede-ti-et","ethiopic-halehame-aa-er","ethiopic-halehame-aa-et","ethiopic-halehame-am-et","ethiopic-halehame-gez","ethiopic-halehame-om-et","ethiopic-halehame-sid-et","ethiopic-halehame-so-et","ethiopic-halehame-ti-er","ethiopic-halehame-ti-et","ethiopic-halehame-tig","ethiopic-numeric","ew-resize","exclusion","expanded","extends","extra-condensed","extra-expanded","fantasy","fast","fill","fill-box","fixed","flat","flex","flex-end","flex-start","footnotes","forwards","from","geometricPrecision","georgian","grayscale","graytext","grid","groove","gujarati","gurmukhi","hand","hangul","hangul-consonant","hard-light","hebrew","help","hidden","hide","higher","highlight","highlighttext","hiragana","hiragana-iroha","horizontal","hsl","hsla","hue","hue-rotate","icon","ignore","inactiveborder","inactivecaption","inactivecaptiontext","infinite","infobackground","infotext","inherit","initial","inline","inline-axis","inline-block","inline-flex","inline-grid","inline-table","inset","inside","intrinsic","invert","italic","japanese-formal","japanese-informal","justify","kannada","katakana","katakana-iroha","keep-all","khmer","korean-hangul-formal","korean-hanja-formal","korean-hanja-informal","landscape","lao","large","larger","left","level","lighter","lighten","line-through","linear","linear-gradient","lines","list-item","listbox","listitem","local","logical","loud","lower","lower-alpha","lower-armenian","lower-greek","lower-hexadecimal","lower-latin","lower-norwegian","lower-roman","lowercase","ltr","luminosity","malayalam","manipulation","match","matrix","matrix3d","media-play-button","media-slider","media-sliderthumb","media-volume-slider","media-volume-sliderthumb","medium","menu","menulist","menulist-button","menutext","message-box","middle","min-intrinsic","mix","mongolian","monospace","move","multiple","multiple_mask_images","multiply","myanmar","n-resize","narrower","ne-resize","nesw-resize","no-close-quote","no-drop","no-open-quote","no-repeat","none","normal","not-allowed","nowrap","ns-resize","numbers","numeric","nw-resize","nwse-resize","oblique","octal","opacity","open-quote","optimizeLegibility","optimizeSpeed","oriya","oromo","outset","outside","outside-shape","overlay","overline","padding","padding-box","painted","page","paused","persian","perspective","pinch-zoom","plus-darker","plus-lighter","pointer","polygon","portrait","pre","pre-line","pre-wrap","preserve-3d","progress","push-button","radial-gradient","radio","read-only","read-write","read-write-plaintext-only","rectangle","region","relative","repeat","repeating-linear-gradient","repeating-radial-gradient","repeating-conic-gradient","repeat-x","repeat-y","reset","reverse","rgb","rgba","ridge","right","rotate","rotate3d","rotateX","rotateY","rotateZ","round","row","row-resize","row-reverse","rtl","run-in","running","s-resize","sans-serif","saturate","saturation","scale","scale3d","scaleX","scaleY","scaleZ","screen","scroll","scrollbar","scroll-position","se-resize","searchfield","searchfield-cancel-button","searchfield-decoration","searchfield-results-button","searchfield-results-decoration","self-start","self-end","semi-condensed","semi-expanded","separate","sepia","serif","show","sidama","simp-chinese-formal","simp-chinese-informal","single","skew","skewX","skewY","skip-white-space","slide","slider-horizontal","slider-vertical","sliderthumb-horizontal","sliderthumb-vertical","slow","small","small-caps","small-caption","smaller","soft-light","solid","somali","source-atop","source-in","source-out","source-over","space","space-around","space-between","space-evenly","spell-out","square","square-button","start","static","status-bar","stretch","stroke","stroke-box","sub","subpixel-antialiased","svg_masks","super","sw-resize","symbolic","symbols","system-ui","table","table-caption","table-cell","table-column","table-column-group","table-footer-group","table-header-group","table-row","table-row-group","tamil","telugu","text","text-bottom","text-top","textarea","textfield","thai","thick","thin","threeddarkshadow","threedface","threedhighlight","threedlightshadow","threedshadow","tibetan","tigre","tigrinya-er","tigrinya-er-abegede","tigrinya-et","tigrinya-et-abegede","to","top","trad-chinese-formal","trad-chinese-informal","transform","translate","translate3d","translateX","translateY","translateZ","transparent","ultra-condensed","ultra-expanded","underline","unidirectional-pan","unset","up","upper-alpha","upper-armenian","upper-greek","upper-hexadecimal","upper-latin","upper-norwegian","upper-roman","uppercase","urdu","url","var","vertical","vertical-text","view-box","visible","visibleFill","visiblePainted","visibleStroke","visual","w-resize","wait","wave","wider","window","windowframe","windowtext","words","wrap","wrap-reverse","x-large","x-small","xor","xx-large","xx-small"],z=i(x),j=a.concat(l).concat(c).concat(p).concat(m).concat(h).concat(w).concat(x);const P={properties:m,colors:w,fonts:f,values:x,all:j},q={documentTypes:n,mediaTypes:s,mediaFeatures:d,mediaValueKeywords:u,propertyKeywords:g,nonStandardPropertyKeywords:b,fontProperties:k,counterDescriptors:y,colorKeywords:v,valueKeywords:z,tokenHooks:{"/":function(e,t){return!!e.eat("*")&&(t.tokenize=_,_(e,t))}}},K=o({name:"css"});function _(e,t){for(var r,o=!1;null!=(r=e.next());){if(o&&"/"==r){t.tokenize=null;break}o="*"==r}return["comment","comment"]}const B=o({name:"scss",mediaTypes:s,mediaFeatures:d,mediaValueKeywords:u,propertyKeywords:g,nonStandardPropertyKeywords:b,colorKeywords:v,valueKeywords:z,fontProperties:k,allowNested:!0,lineComment:"//",tokenHooks:{"/":function(e,t){return e.eat("/")?(e.skipToEnd(),["comment","comment"]):e.eat("*")?(t.tokenize=_,_(e,t)):["operator","operator"]},":":function(e){return!!e.match(/^\s*\{/,!1)&&[null,null]},$:function(e){return e.match(/^[\w-]+/),e.match(/^\s*:/,!1)?["def","variable-definition"]:["variableName.special","variable"]},"#":function(e){return!!e.eat("{")&&[null,"interpolation"]}}}),C=o({name:"less",mediaTypes:s,mediaFeatures:d,mediaValueKeywords:u,propertyKeywords:g,nonStandardPropertyKeywords:b,colorKeywords:v,valueKeywords:z,fontProperties:k,allowNested:!0,lineComment:"//",tokenHooks:{"/":function(e,t){return e.eat("/")?(e.skipToEnd(),["comment","comment"]):e.eat("*")?(t.tokenize=_,_(e,t)):["operator","operator"]},"@":function(e){return e.eat("{")?[null,"interpolation"]:!e.match(/^(charset|document|font-face|import|(-(moz|ms|o|webkit)-)?keyframes|media|namespace|page|supports)\b/i,!1)&&(e.eatWhile(/[\w\\\-]/),e.match(/^\s*:/,!1)?["def","variable-definition"]:["variableName","variable"])},"&":function(){return["atom","atom"]}}}),O=o({name:"gss",documentTypes:n,mediaTypes:s,mediaFeatures:d,propertyKeywords:g,nonStandardPropertyKeywords:b,fontProperties:k,counterDescriptors:y,colorKeywords:v,valueKeywords:z,supportsAtComponent:!0,tokenHooks:{"/":function(e,t){return!!e.eat("*")&&(t.tokenize=_,_(e,t))}}})}}]);
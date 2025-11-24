import {marked} from "marked";
import Katex from "katex";
import extendedLatex from "marked-extended-latex";
const spoiler = {
  name: "spoiler",
  level: "block", //is this a block-level or inline-level tokenizer?
  start(src) {
    return src.match(/^!!!/)?.index;
  }, //hint to Marked.js to stop and check for a match
  tokenizer(src, tokens) {
    const rule = /^!!!(.|\n)*?!!!/; //regex for the complete token, anchor to string start
    const match = rule.exec(src);
    if (match) {
      let text = match[0].replace(/(^!!!)|(\n!!!)/g, "");
      let label = /^.*\n/.exec(text)[0].trim();
      text = text.slice(label.length);

      const token = { //token to generate
        type: "spoiler", //should match "name" above
        raw: match[0], //text to consume from the source
        text: text.trim(), //additional custom properties, including
        label: label || "spoiler",
        tokens: [],
      };
      this.lexer.blockTokens(token.text, token.tokens); //queue this data to be processed for inline tokens
      return token;
    }
  },
  renderer(token) {
    return `\n<div class="mdSpoiler hidden"><div class="mdSpoilerLabel">${token.label}</div>${this.parser.parse(token.tokens)}</div>`;
  },
  childTokens: [], //any child tokens to be visited by walkTokens
};

marked.use({ extensions: [spoiler] });
marked.use(extendedLatex({
  render: (formula, displayMode) => Katex.renderToString(formula, { displayMode }),
}));

//add support for prefixing links with "blank:" to open in new tab
const renderer = new marked.Renderer();
const linkRenderer = renderer.link;
renderer.link = (href, title, text) => {
  if (href.startsWith("blank:")) {
    let newHref = href.slice(6);
    const html = linkRenderer.call(renderer, newHref, title, text);
    return html.replace(/^<a /, "<a target=\"_blank\"");
  }

  return linkRenderer.call(renderer, href, title, text);
};


function renderMarkdown(markdown){
  return marked(markdown, { renderer });
}
export default renderMarkdown;

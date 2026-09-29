# 安装与调用

## macOS 安装

1. 双击 `dist/DalalaSongchiPaint-Regular-v0.2.ttf`。
2. 在字体册中点击“安装字体”。
3. 重新打开需要调用字体的软件。
4. 字体菜单中搜索 `Dalala Songchi Paint`。

## 网页工作台

```css
@font-face {
  font-family: "Dalala Songchi Paint";
  src: url("./DalalaSongchiPaint-Regular-v0.2.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

连续输入“看看”时，支持 `calt` 的排版引擎会自动使用第二个“看”。也可以通过 `ss01` 手动调用替换字形。

当前属于局部字库。只建议输入清单中已覆盖的字符；未覆盖字符必须先扩字，避免软件自动混入其他字体。


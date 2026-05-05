---
title: "Why Mathematica does not simplify Sinh[ArcCosh[x]]"
source: "https://www.johndcook.com/blog/2026/03/10/sinh-arccosh/"
author:
  - "[[John]]"
published: 2026-03-10
created: 2026-04-10
description: "When Mathematica seems to not to know how to simplify an expression, it may be doing the right thing, being more sophisticated than you expect."
tags:
  - "clippings"
---
I’ve written several posts about applying trig functions to inverse trig functions. I intended to write two posts, one about the [three basic trig functions](https://www.johndcook.com/blog/2026/02/25/trig-of-inverse-trig/) and one about their [hyperbolic counterparts](https://www.johndcook.com/blog/2026/02/25/hyperbolic-versions-of-latest-posts/). But there’s more to explore here than I thought at first. For example, the mistakes that I made in the first post lead to a couple more posts discussing error detection and proofs.

I was curious about how Mathematica would handle these identities. Sometimes it doesn’t simplify expressions the way you expect, and for interesting reasons. It handled the circular functions as you might expect.

![\renewcommand{\arraystretch}{2.2} \begin{array}{c|c|c|c} & \sin^{-1} & \cos^{-1} & \tan^{-1} \\ \hline \sin & x & \sqrt{1-x^{2}} & \dfrac{x}{\sqrt{1+x^2}} \\ \hline \cos & \sqrt{1-x^{2}} & x & \dfrac{1}{\sqrt{1 + x^2}} \\ \hline \tan & \dfrac{x}{\sqrt{1-x^{2}}} & \dfrac{\sqrt{1-x^{2}}}{x} & x \\ \end{array}](https://www.johndcook.com/trig_of_inverse4.svg)

So, for example, if you enter `Sin[ArcCos[x]]` it returns √(1 − *x* ²) as in the table above. Then I added an *h* on the end of all the function names to see whether it would reproduce the table of hyperbolic compositions.

![\renewcommand{\arraystretch}{2.2} \begin{array}{c|c|c|c} & \sinh^{-1} & \cosh^{-1} & \tanh^{-1} \\ \hline \sinh & x & \sqrt{x^{2}-1} & \dfrac{x}{\sqrt{1-x^2}} \\ \hline \cosh & \sqrt{x^{2} + 1} & x & \dfrac{1}{\sqrt{1 - x^2}} \\ \hline \tanh & \dfrac{x}{\sqrt{x^{2}+1}} & \dfrac{\sqrt{x^{2}-1}}{x} & x \\ \end{array} ](https://www.johndcook.com/hyp_mult_table.svg)

For the most part it did, but not entirely. The results were as expected except when applying sinh or cosh to arccosh. But `Sinh[ArcCosh[x]]` returns

![\sqrt{\frac{x-1}{x+1}} (x+1)](https://www.johndcook.com/sinh_arccosh1.svg)

and `Tanh[ArcCosh[x]]` returns

![\frac{\sqrt{\frac{x-1}{x+1}} (x+1)}{x}](https://www.johndcook.com/tanh_arccosh1.svg)

## Why doesn’t Mathematica simplify as expected?

Why didn’t `Sinh[ ArcCosh[x] ]` just return √(*x* ² − 1)? The expression it returned is equivalent to this: just square the (*x* + 1) term, bring it inside the radical, and simplify. That line of reasoning is correct for some values of *x* but not for others. For example, `Sinh[ArcCosh[2]]` returns −√3 but √(2² − 1) = √3. The expression Mathematica returns for `Sinh[ArcCosh[x]]` correctly evaluates to −√3.

## Defining ArcCosh

To understand what’s going on, we have to look closer at what arccosh(*x*) means. You might say it is a function that returns the number whose hyperbolic cosine equals *x*. But cosh is an even function: cosh(− *x*) = cosh(*x*), so we can’t say *the* value. OK, so we define arccosh(*x*) to be the *positive* number whose hyperbolic cosine equals *x*. That works for real values of *x* that are at least 1. But what do we mean by, for example, arccosh(1/2)? There is no real number *y* such that cosh(*y*) = 1/2.

To rigorously define inverse hyperbolic cosine, we need to make a branch cut. We cannot define arccosh as an analytic function over the entire complex plane. But if we remove (−∞, 1\], we can. We define arccosh(*x*) for real *x* > 1 to be *the* positive real number *y* such that cosh(*y*) = *x*, and define it for the rest of the complex plane (with our branch cut (−∞, 1\] removed) by analytic continuation.

If we look up `ArcCosh` in Mathematica’s documentation, it says “ArcCosh\[z\] has a branch cut discontinuity in the complex z plane running from −∞ to +1.” But what about values of *x* that lie on the branch cut? For example, we looked at `ArcCosh[-2]` above. We can extend arccosh to the entire complex plane, but we cannot extend it as an analytic function.

So how do we define arccosh(*x*) for *x* in (−∞, 1\]? We could define it to be the limit of arccosh(*z*) as *z* approaches *x* for values of *z* not on the branch cut. But we have to make a choice: do we approach *x* from above or from below? That is, we can define arccosh(*x*) for real *x* ≤ 1 by

or by

but we have to make a choice because the two limits are not the same. For example, `ArcCosh[-2 + 0.001 I]` returns `1.31696 + 3.14102 I` but `ArcCosh[-2 - 0.001 I]` returns `1.31696 - 3.14102 I`. By convention, we choose the limit from above.

## Defining square root

Where did we go wrong when we assumed Mathematica’s expression for sinh(arccosh(*x*))

![\sqrt{\frac{x-1}{x+1}} (x+1)](https://www.johndcook.com/sinh_arccosh1.svg)

could be simplified to √(*x* ² − 1)? We implicitly assumed √(*x* + 1)² = (*x* + 1). And that’s true, if *x* ≥ − 1, but not for smaller *x*. Just as we have be careful about how we define arccosh, we have to be careful about how we define square root.

The process of defining the square root function for all complex numbers is analogous to the process of defining arccosh. First, we define square root to be what we expect for positive real numbers. Then we make a branch cut, in this case (−∞, 0\]. Then we define it by analytic continuation for all values not on the cut. Then finally, we define it along the cut by continuity, taking the limit from above.

Once we’ve defined arccosh and square root carefully, we can see that the expressions Mathematica returns for sinh(arccosh(*x*)) and tanh(arccosh(*x*)) are correct for all complex inputs, while the simpler expressions in the table above implicitly assume we’re working with values of *x* for which arccosh(*x*) is real.

## Making assumptions explicit

If we are only concerned with values of *x* ≥ − 1 we can tell Mathematica this, and it will simplify expressions accordingly. If we ask it for
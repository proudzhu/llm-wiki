*NB: The title of this post is an intentional clickbait. Even though I do stand for its statement, a more honest one would be something like: It's NOT OK to compare floating-points using epsilons.*

You've probably heard the mantra that you must never compare floating-point numbers for exact equality, and you absolutely must use some kind of epsilon-comparison instead, like

```cpp
bool approxEqual(float x, float y)
{
    return abs(x - y) < 1e-4f;
}
```

Over the 15+ years that I've been writing code, – which often deals with geometry, graphics, physics, simulations, etc, and thus has to work with floating-points on a daily basis, – I've encountered only one or two cases where such epsilon-comparison is actually a good solution. Pretty much always there is a better solution that either involves rewriting the code in some way, or simply compares floating-points just like `x == y`. And pretty much always the epsilon solution was actually one of the *worst* possible options.

I'll show a bunch of examples where adding some kind of epsilon might be your first instinct, but actually a much better – and often much simpler – solution exists. But first, let's talk about floating-point numbers.

## Contents

## Floating-points are not a black box

The whole idea of epsilon-comparison seems to come from the general perception of floating-point numbers as some kind of random black-box machine that sometimes produces inexact results because the gods of computing force it to. In reality it is a pretty deterministic (modulo compiler options, CPU flags, etc) and [highly standardized](https://en.wikipedia.org/wiki/IEEE_754) system.

Floating-point numbers are necessarily inexact in that they cannot represent all possible real numbers. In fact, no finite amount of memory can, because that's how maths works – there are just [way too many](https://en.wikipedia.org/wiki/Cardinality_of_the_continuum) real numbers (or even just rational numbers, fwiw). Given that we probably only want to allocate a fixed (and not just a finite) amount of bits per such a number, we're forced to accept that only a finite set of numbers will be representable (specifically, at most $2^{bits}$ of them), and for all others we'll have to deal with approximations.

I don't want this to turn into a lecture on how floating-point numbers are represented, though; I think [wikipedia](https://en.wikipedia.org/wiki/Floating-point_arithmetic) does a good enough job. For a more in-depth source, see [this classic](https://www.itu.dk/~sestoft/bachelor/IEEE754_article.pdf) by David Goldberg, or [this more recent one](https://www.phys.uconn.edu/~rozman/Courses/P2200_15F/downloads/floating-point-guide-2015-10-15.pdf) that follows the same idea. What's more important is that this "inexactness" of floating-point numbers doesn't mean some "uncertainty" or "randomness" in its behavior!

For example, any single arithmetic operation (e.g. addition, multiplication, etc) on two floating-point numbers is required to produce a floating-point number which is the closest to the actual true answer if we treat the inputs as being exact (there are some rounding rules in case of ties, i.e. when two representable numbers are equally close to the true answer). Notice that, even though the result is approximate, it is still guaranteed to be as close to the truth as possible, and is very much deterministic.

However, it does mean that our usual mathematical formulas don't always hold for floating-points. For example, even though addition (and multiplication) are guaranteed to be *commutative* ($a + b = b + a$), they aren't necessarily *associative*: it may happen that $(a+b)+c\neq a+(b+c)$. It's fairly easy to find such examples; [here's one](https://godbolt.org/z/jvdo8j4fv) that works for 32-bit floating-points:

```cpp
// Outputs 0.89999998
std::cout << std::setprecision(8) << ((0.2f + 0.3f) + 0.4f) << '\n';

// Outputs 0.90000004
std::cout << std::setprecision(8) << (0.2f + (0.3f + 0.4f)) << '\n';
```

Notice that, even though the expressions aren't equal, they are very close (the difference is about 6e-8), and the floating-point standard has some guarantees that we can use to *predict* how large the difference can be.

So, what's the problem, then? We know that the result of some computation is only approximate, and we compare it with some expected result approximately, sounds about right.

Or does it?

## Problems with epsilons

I have 3 major problems with those epsilon-comparisons:

1. They are a hacky, temporary solution,
2. They often cascade into extremely hard-to-debug issues, and
3. They often don't solve the initial problem.

The second point is probably the toughest. One part of the program treats 2D points as equal if they are separated in [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) by no more than 1e-4, another part of the program treats points as equal if they are separated in L-inf distance (max of coordinates) by no more than 1e-6, the input points themselves are generated using some other algorithm, and now all the input-output invariants are messed up, and your line rendering is broken but only in this specific scenario, with this specific data, only at night and in full moon. Good luck debugging that.

A rare wrong case of line rendering isn't that much of an issue, but it can manifest in a ton of other ways, up to crashing the program, and can be really nasty when combined with a lot of other geometric code. I've encountered many such cases, and mismatched epsilon comparisons were an extremely common root cause.

The problem is that these epsilons are pretty much always simply *guessed*, and there is no correct way to choose one epsilon out of many. If you have several such comparisons, no combination of epsilons will ensure that everything works correctly.

Another problem with epsilons is that such comparison isn't [transitive](https://en.wikipedia.org/wiki/Transitive_relation). This might sound like a technical nitpick, but in reality most algorithms assume that things like comparisons are in fact transitive, and these algorithms can simply break (produce nonsense or even crash) if you use a non-transitive comparison with them.

So, what should we do, then? We need to *think* about the problem! Shocking, I know. Why are we comparing floating-points in the first place? Maybe we don't trust our algorithms? Maybe we don't trust the data? Maybe we don't trust the CPU? There's no single answer, so let's look at some examples.

## Case in study: grid-based movement

Say, you have a turn-based game where units move on a grid. A unit has some movement points and can do several moves per turn, but for UX sake you only allow executing the next move after the previous one finished.

Now, you're probably interpolating the unit's position somehow and not just teleporting it to the target grid cell, so you need to check when exactly the move is finished before allowing the player to select the next move target.

You could just wait for a certain amount of time (and that would be a perfectly good solution in many cases!), but different units have different animations and thus different timings, there are some accessibility settings to reduce animations, etc, so you decide that relying on animation time isn't a good idea.

Then you realize that the move finishes exactly when the position of the unit coincides with the target cell's center. You write something like

```cpp
void update() {
    if (selectedUnit.position != targetCell.center)
        return;

    // Do the frame update
}
```

and after the move was executed, nothing happens and the game effectively hangs, because the condition `selectedUnit.position != targetCell.center` is never true. With a typical linear interpolation with easing, the code

```cpp
vec2f getPosition(float time) {
    return lerp(start, end, easing(time));
}
```

will produce enough floating-point roundings that the result will never be equal to `end` when `time == 1.f`. Heck, in [some interpolation schemes](https://lisyarus.github.io/blog/posts/exponential-smoothing.html) it's not even supposed to be ever true!

Damn, stupid floating-points! — you grumble as you add the holy grail of floating-points — an epsilon-comparison:

```cpp
void update() {
    if (distance(selectedUnit.position, targetCell.center) > 1e-4)
        return;

    // Do the frame update
}
```

This solves the issue, so why is this so bad? For a number of reasons:

- The specific epsilon of `1e-4` might break if you decide to choose a different interpolation scheme
- As always with epsilons, someone reading the code will get confused and suspicious
- Making the player wait is one of the worst things you can do

So, how do we solve this? One option is to use some sort of acceptance radius: once the unit is within, say, `0.25` of the target cell's center, we stop the animation and allow the player to issue the next commands. Then, we find the actually good value by a lot of testing.

How is this different from epsilons? It isn't really, except that now it's at least backed by something instead of being a random value. The real problem here is mixing the *data model* with its *presentation*. The internal doings of the game's state machine shouldn't care about where some 3D model is located. That's usually harder than it seems (which is roughly why UX is even a thing), but very much doable.

In this case, the best solution (in my opinion!) is to allow the user to issue commands without waiting for the unit to complete its movement in the first place. Once a user clicks on some grid cell, the rendering gets notified that a movement must take place, while the internal model of the game's state thinks that the unit is already on the next cell.

There are many ways to implement that, e.g. by queuing the requested animations and playing them one-by-one, or using an [animation/interpolation scheme](https://lisyarus.github.io/blog/posts/exponential-smoothing.html) that is robust against sudden changes in the target value. What's important is that it is very doable, relatively straightforward, and doesn't require epsilons.

## Case in study: spherical linear interpolation

[Spherical linear interpolation](https://en.wikipedia.org/wiki/Spherical_linear_interpolation) is a way to interpolate points on a sphere (aka unit vectors) in such a way that the interpolated vector follows a curve with a fixed rotation speed. A simple `normalize(lerp(a, b, t))` won't cut it — the resulting vector moves slower near the ends and faster in the middle. Here's a [cool visualization](https://splines.readthedocs.io/en/latest/rotation/slerp.html) of slerp. Quite often this function is only implemented for quaternions, but it's useful for any vectors of any dimension (though in case of quaternions it differs a bit because $q$ and $-q$ represent the same rotation).

Quite conveniently, if the input vectors are normalized, it boils down to a pretty straightforward formula:

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float angle = acos(dot(a, b));
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

Now, from time to time this code will produce `NaN` s, for a couple of reasons:

- Even if the vectors are normalized, their dot product can produce values outside of the $[-1, 1]$ range, and `acos` will return `NaN`
- When the input vectors are very close, `angle` can become zero, and division of zero by zero will once again produce `NaN`

The first problem is easy to deal with: just wrap `acos` argument in `clamp`:

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float angle = acos(clamp(dot(a, b), -1.f, 1.f));
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

The second problem is more subtle. Thankfully, when the `angle` is small enough, spherical linear interpolation turns into usual linear interpolation, so we can detect this case and switch to usual `lerp(a, b, t)` instead. But how small is small enough?

It's tempting to just throw some epsilon here, like

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float angle = acos(dot(a, b));
    if (angle < 1e-4) {
        return lerp(a, b, t);
    }
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

However, this makes the code less precise than it could be, even if the resulting vector is still close to what we expect it to be. And, once again, a random epsilon always raises the question of how this exact value was chosen. We can do better!

Both [glm](https://github.com/g-truc/glm/blob/6f14f4792a0cde5d0cf2c910506724d61cb95834/glm/ext/quaternion_common.inl#L41) and [Eigen](https://github.com/PX4/eigen/blob/7cf1c0179eb0f5499dfc1bffbd229783a7865fe1/Eigen/src/Geometry/Quaternion.h#L726) use a reasonable check:

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float d = dot(a, b);
    if (d > 1.f - FLT_EPSILON) {
        return lerp(a, b, t);
    }
    float angle = acos(dot(a, b));
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

Here, `FLT_EPSILON` is exactly $2^{-23}$ — the smallest single-precision floating-point value $x$ such that $1 + x \neq x$ (using floating-point addition). Honestly, it doens't feel much better than a random epsilon to me — throwing `FLT_EPSILON` doesn't solve our issues unless we've proved that this is the exact threshold that works in our case.

Let's analyze the code. The main problem is that `angle` being zero causes `NaN` 's. The secondary problem is that `angle` being too small might introduce precision errors.

Let's think about precision first. `angle` isn't just an arbitrary number — it's the result of calling `acos`, and we're worried about the case when the argument to `acos` is close to 1. In fact, the `angle` itself is somewhat irrelevant, as we mostly care anout `sin(angle)`, not the angle itself.

Now, $\sin(\operatorname{acos}(x))$ is just $\sqrt{1-x^2}$. In our case, `x = dot(a, b)`. When $x = 1 - \varepsilon$, we have

$$
\sin(\operatorname{acos}(x)) = \sqrt{1-x^2} = \sqrt{1-(1-\varepsilon)^2} = \sqrt{2\varepsilon-\varepsilon^2} \approx \sqrt{2\varepsilon}
$$

The $\varepsilon^2$ term is too small to care about, and $\sqrt 2$ is just a constant close to 1. The main thing here is $\sqrt{\varepsilon}$: even if $\varepsilon$ is something as small as `FLT_EPSILON`, the `sin(angle)` term will be something like the square root of it. For small numbers, square root increases the number significantly. For example, while `FLT_EPSILON` is around `1.2e-07`, its square root is around `3.5e-04`, i.e. about 2000 times larger.

All I'm trying to say here is: in the case we care about, the argument to `acos` is close to 1, so the difference between possible representable values of the argument to `acos` is a much more serious source of precision problems compared to the angle itself being close to zero.

*Actually, the smallest value less than 1 that is representable in floating-point is not `1 - FLT_EPSILON`, but `1 - FLT_EPSILON / 2.f`, which somewhat supports my argument that the `FLT_EPSILON` constant was chosen somewhat arbitrarily here.*

So, unless we want something special, we can ignore that the angle can be small in terms of precision, and focus on obtaining `NaN`. In this code, provided that the arguments are finite values, the only way to get a `NaN` is with division by zero, which can occur only when the `angle` is zero, which can occur only when `dot(a, b) >= 1`. As we've discussed, the next smallest representable value of `dot(a, b)` is `1 - FLT_EPSILON / 2.f`, with the `angle` being roughly `sqrt(FLT_EPSILON)`, which is around `3.5e-04` — a rather large floating-point value considering that the whole range is about `[1e-38 .. 1e38]`, so we can be sure that even a half-decent implementation of `acos` wouldn't return zero in this case.

Thus, in case `dot(a, b) < 1`, we're actually fine! The only thing to check is if `dot(a, b) == 1`, or, combining with the `clamp` we added earlier, if `dot(a, b) >= 1`:

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float d = dot(a, b);
    if (d >= 1.f) {
        return lerp(a, b, t);
    }
    float angle = acos(dot(a, b));
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / sin(angle);
}
```

*(Note that I've intentionally left out the case when the dot product is close to $-1$: in that case, there's no unique solution to the interpolation problem, and it's better dealt with separately.)*

Alternatively, we can check `sin(angle)` directly, though this means we can't save on the expensive `acos` call in the corner case:

```cpp
vec3 slerp(vec3 a, vec3 b, float t) {
    float angle = acos(clamp(dot(a, b), -1.f, 1.f));
    float s = sin(angle);
    if (s == 0.f) {
        return lerp(a, b, t);
    }
    return (sin((1 - t) * angle) * a + sin(t * angle) * b) / s;
}
```

## Case in study: computing vector length

You wouldn't be surprised if I told you that computing the (Euclidean) length of a vector is a fairly common and useful operation. The implementation is rather straightforward:

```cpp
float length(vec3 v) {
    return sqrt(dot(v, v));
}
```

or, if we inline the `dot` call,

```cpp
float length(vec3 v) {
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}
```

You've probably seen this a dozen times, so what's wrong with it? Nothing really, except that for really small vectors (those having length around `1e-19`) it returns zero, and for larger vectors we get a significant precision loss. Even if the result is a perfectly valid floating-point value, its square (i.e. the expression under the square root) can be too small to be adequately representable in floating-point.

So what? There are hardly any use cases when such a vector is indistinguishable from zero anyway. However, an invariant saying that only the zero vector has zero length would be extremely convenient, and would simplify writing code in a lot of cases, especially when we want to treat floating-points carefully.

There's actually a very simple way to do that: compute the maximum `M` of the absolute values of vector coordinates, then return `M * length(v / M)`. Thanks to floating-point guarantees, one of the coordinates will be at least 1, so the expression under the square root is at least 1, and at most $D$ — the dimension (3 in case of `vec3`).

So, the code turns into

```cpp
float length(vec3 v) {
    float M = max(abs(v.x), abs(v.y), abs(v.z));
    vec3 u = v / M;
    return M * sqrt(u.x * u.x + u.y * u.y + u.z * u.z);
}
```

That's [about twice as many](https://godbolt.org/z/Ef4b1h96r) assembly instructions, but unless this happens in a hot loop, I'd say it's worth the extra precision and safety.

The only problem is that if the vector is zero (yes, literally zero, not just small), this function returns `NaN`! However, if at least one of the vector's coordinates is non-zero (even if it is a subnormal value), `M` will be strictly larger than zero, and the algorithm will work correctly (and never with less precision than the naive version). So, the correct fix is literally comparing `M` to zero:

```cpp
float length(vec3 v) {
    float M = max(abs(v.x), abs(v.y), abs(v.z));
    if (M == 0.f) return 0.f;
    vec3 u = v / M;
    return M * sqrt(u.x * u.x + u.y * u.y + u.z * u.z);
}
```

If we'd write `if (M < 1e-4)` instead, we'd basically destroy the reason this function exists in the first place.

## Case in study: solving linear systems

You wouldn't be surprised if I told you that solving linear systems of equations is a fairly common and useful operation. Half of physics & engineering problems boil down to solving some linear systems (the other half being eigenvalue equations).

For a general non-sparse system, there's basically the only standard way to solve it: the Gauss-Jordan elimination. *(Actually, we can also use QR decomposition — afaik it's slower but more numerically stable.)* The general algorithm is rather long, but not too complicated — it's just a bunch of `for` loops and some arithmetics on the coefficients of the system.

What's important is that the algorithm can be [rather unstable](https://en.wikipedia.org/wiki/Gaussian_elimination#Numeric_instability): at some point you take top-left entry of the remaining part of the matrix, and divide the whole row with that entry. If it was small, the floating-point errors from cancellation are amplified, and if it is zero, you get `NaN` 's.

However, the algorithm becomes stable in practice (the instabilities are extremely rare and typically theoretical) if instead we do something called *partial pivoting*: find the row with the largest (in absolute value) coefficient in the current column, and use that row instead of the original top row. It complicates the algorithm somewhat, but makes it very much usable in practice.

The only problem is that we're still dividing, and potentially dividing by something very small or even zero! There isn't some clever way to escape this: a matrix can be *singular*, in which case maths tells us that there's no solution at all.

So, first of all our routine should return an `optional<vector>`, and secondly we need to check for this division:

```cpp
optional<vector> solve(matrix const& m, vector const& v) {
    // Gaussian elimitation code...

    for (int i = 0; i < m.columns(); ++i) {

        // Find maximum m[j][i] among all remaining rows
        float M = 0.f;
        for (int j = i; j < m.rows(); ++j)
            M = max(M, abs(m[j][i]));

        if (M < 1e-4)
            return std::nullopt;

        // Proceed with the algorithm
    }
}
```

Now, obviously this `1e-4` comes from nowhere — a classic epsilon placed simply to make the problem shut up instead of solving it.

For some systems that are close to being singular, our algorithm will report that it failed, based on a pretty much arbitrary threshold. Even worse, this `M` value we computed isn't some inherent property of the matrix, but simply an intermediate value we obtained with our algorithm.

This threshold should absolutely be at least provided by the user themselves (maybe with a default parameter), but that's still rather quiestionable. Proper ways of checking whether a matrix is singular or close to singular is computing its [condition number](https://en.wikipedia.org/wiki/Condition_number#Matrices) or inspecting its [singular values](https://en.wikipedia.org/wiki/Singular_value), not setting an arbitrary threshold on an arbitrary intermediate value!

My point is: it's not our job to figure out how singular the matrix is, it's the user's job. Our job, as implementors of the Gauss-Jordan elimination algorithm, is to provide an answer that is as good as we can get, or report that we failed otherwise. The only way our code can truly fail is by dividing zero by zero — everything else will give some reasonable answer, even if very imprecise (depending on the matrix).

So, in my opinion, the correct code would be just

```cpp
// ...

if (M == 0.f)
    return std::nullopt;

// ...
```

*To be honest, this still doesn't prevent us from dividing something large by something small and getting infinities, — but no epsilon protects against that either.*

## Case in study: ray-box intersection

Whenever you're making a raytracer (voxel or otherwise), or implementing object picking by mouse, or doing any of a million other things, you'll need a ray-box intersection routine.

The algorithm itself is pretty straightforward: you compute the time (i.e. the parameter $t$ along the ray $o+t\cdot d$) when the ray enters the box and the time it leaves the box. If the former is less than the latter, that's your intersection. You compute the enter time as the maximum of enter times along each of the coordinates; similarly, the leave time is the minimum along each of the coordinates.

[This scratchapixel article](https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection.html) explains it quite well. The code looks roughly like this:

```cpp
void sort(float & x, float & y) {
    if (x > y) swap(x, y);
}

pair<float, float> intersect(ray r, box b) {
    float txmin = (b.min.x - r.origin.x) / r.direction.x;
    float txmax = (b.max.x - r.origin.x) / r.direction.x;
    float tymin = (b.min.y - r.origin.y) / r.direction.y;
    float tymax = (b.max.y - r.origin.y) / r.direction.y;
    float tzmin = (b.min.z - r.origin.z) / r.direction.z;
    float tzmax = (b.max.z - r.origin.z) / r.direction.z;

    sort(txmin, txmax);
    sort(tymin, tymax);
    sort(tzmin, tzmax);

    float tmax = min(txmax, min(tymax, tzmax));
    float tmin = max(txmin, min(tymin, tzmin));

    return {tmin, tmax};
}
```

*NB: if we [rewrite](https://godbolt.org/z/aGK3oaav9) `sort` a bit, we can force it to use `minss/maxss` SSE instructions, thus making the `intersect` function branchless.*

It's a pretty short, readable function, and in 99.99% of cases it works perfectly. Yet, once in a while you'll end up with a ray that has `direction.x` equal to zero, thus the divide will give infinities or `NaN` 's. Oops!

So, let's add some epsilons, right? No. First of all, what are you going to do if `abs(direction.x) < 1e-4`? You still need to add some code that finds the intersection properly but doesn't divide by `direction.x`, and it might just work without epsilons anyway.

Let's analyze the code! What happens if `direction.x == 0`? The ray is parallel to the YZ plane, so the real intersection happens there. But we can't just ignore the X coordinate: if the ray starts outside the `[b.min.x, b.max.x]` interval, there's no intersection, otherwise we need to inspect the Y and Z coordinates.

What happens exactly when `direction.x == 0`? When you divide `A / direction.x`, it returns $-\infty$ if `A < 0` and $\infty$ if `A > 0`. In our case, `A` is `b.min.x - r.origin.x` or `b.max.x - r.origin.x`. So, if the ray origin `r.origin.x` is inside the interval `[b.min.x, b.max.x]`, we'll get `txmin == -INF` and `txmax == INF`. If the ray origin is outside of this interval, both `txmin` and `txmax` will both be either `-INF` or `INF`.

If there is an intersection and the origin is within the interval, the calculation of `tmin` will effectively ignore the value of `txmin == -INF`, because it's always true that `max(-INF, x) == x`. Similarly, `tmax` will effectively ignore `txmax == INF`. In this case, the code will just compute the correct intersection in the YZ plane, as required.

If, however, the origin is not within the interval, either `txmin == txmax == INF`, leading to `tmin == INF` but `tmax` being some finite value, leading to no intersection (because `tmin > tmax`), or `txmin == txmax == -INF`, leading to `tmax == -INF` but `tmin` being some finite value, leading to no intersection again.

All this is to say that our code actually *works correctly* in case `direction.x == 0`! No epsilons needed, it already handles the infinities exactly as it should. Or does it?

We've forgotten that in IEEE754 there are two zeros: a positive `+0` and a negative `-0` one. Dividing by the negative zero produces infinity, but also flips the sign! So, we can get a case when `txmin == INF` and `txmax == -INF`, leading to no intersection being reported even if there is one.

Thankfully, our `sort(txmin, txmax)` call solves this issue, swapping these into the case of `txmin == -INF` and `txmax == INF`! So, once again, our code already works correctly in this case.

*The Scratch-a-pixel link above also discusses a solution to this problem, which has a whole ton of if's making it not branchless but also able to do an early-out.*

Actually, there's one more case we didn't fix yet: if both `r.direction.x == 0` and `r.origin.x == b.min.x`, we'll get zero divided by zero, i.e. a `NaN`. Unfortunately, our code doesn't automatically solve this: `NaN` compared to anything always returns `false`, so, depending on how `sort`, `min` and `max` are implemented, we might end up with `tmin` or `tmax` being `NaN`, which effectively means no intersection. This might be OK for your use-case, but I don't know a simple way to fix that if we want this to be reported as a true intersection. We could just check if `r.direction.x == 0 && r.origin.x == b.min.x` and set `tmin = -INF` in this case, but the code stops being branchless. This happens extremely rarely in practice, though, so we might just get away with it:)

## Case in study: computing convex hull

Most 2D convex hull algorithms eventually boil down to checking whether, for three points $A, B, C$, the last point $C$ lies to the left of the ray $AB$. Equivalently, it asks whether when moving from $A$ to $B$ and then turning to move from $B$ to $C$, you make a left turn or a right turn. This is why this predicate is often called `left_turn`.

It boils down to checking the relative orientation of two vectors $AB$ and $AC$, and can be computed by a simple determinant:

```cpp
float det(vec2 a, vec2 b) {
    return a.x * b.y - a.y * b.x;
}

bool left_turn(vec2 a, vec2 b, vec2 c) {
    return det(b - a, c - a) > 0.f;
}
```

It's pretty cool that you can put all your floating-point stuff inside this predicate — the convex hull algorithm itself doesn't care about the coordinates and can operate just as an abstract algorithm, provided you have this `left_turn` predicate as some kind of a black box.

However, it turns out that most of computational geometry algorithms are extremely sensitive to edge cases, and can completely break if such an edge case breaks certain invariants of this algorithm.

For the `left_turn` predicate, one such invariant is that it doesn't change when we cycle the points:

```cpp
left_turn(A,B,C) == left_turn(B,C,A) == left_turn(C,A,B)
```

It's pretty easy to find three points *almost* on the same line that break this invariant. It happens so often that any convex hull algorithm that is supposed to handle at least some 1000 points must take this into account.

We know the solution, right? — just slap an epsilon here:

```cpp
bool left_turn(vec2 a, vec2 b, vec2 c) {
    return det(b - a, c - a) > 1e-4f;
}
```

Well, of course it doesn't work. Floating-point errors can easily lead to this predicate violating the cyclic invariant above.

There are many ways of solving this problem:

- Round the input values to some fixed grid, then work with integers instead
- Use [arbitrary precision](https://github.com/boostorg/multiprecision) rational arithmetic to get the true result
- Use CPU-rounding-flags-backed [interval arithmetic](https://www.boost.org/doc/libs/latest/libs/numeric/interval/doc/interval.htm) to compute the result; resort to arbitrary precision if it fails
- Knowing exact IEEE754 rounding rules, compute an upper bound on the possible error, compare with the naive result, and return if the error is smaller than the result; otherwise, use any of the more precise methods
- Use some variation of the [2Sum](https://en.wikipedia.org/wiki/2Sum) algorithm to compute the result; use any of the more precise methods if it fails

Of all these, the first option (round to a fixed grid) is probably the simplest and the most practical. However, there are cases when you can't do that, and you need to work with the unperturbed input data, and you need more complex methods. In any case, no epsilons will save you — sooner or later your algorithm will return nonsense, or will simply crash.

*Note that, in any case, such a predicate is better thought of as returning three possible values: left, right, and collinear (or -1, 0, and 1, if you're feeling '90s). This is very similar to [three-way comparison](https://en.wikipedia.org/wiki/Three-way_comparison).*

## Case in study: sanitizing user input

The last two cases will be the ones where I think epsilons are actually a good solution!

Say, you're writing some geometry visualization library, or maybe some cartographic engine of sorts. The user supplies you with a polyline that you can't control. You task is to perform some computations on it, and maybe to render it.

Now, rendering polylines is a pretty complicated topic; in particular, we typically triangulate the polyline using various types of [joins](https://ivan.sanchezortega.es/development/2023/02/06/reinventing-line-joins.html) and caps. And to compute these, we need various things like the normal to a particular line segment, or the angle between two consecutive line segments. And, of course, everything breaks if two consecutive line points are equal or simply too close — normal & angle calculations go way off, introducing ugly artifacts to our lovely line.

Now, we could say that consecutive equal points are not allowed, which would be a reasonable requirement for some library or algorithm, but not so much for a user-facing engine/framework. After all, filtering out equal points is easy — literally a single call to [`std::unique`](https://en.cppreference.com/w/cpp/algorithm/unique.html). But what are we going to do with points that are just too close, but not equal?

Mathematically, having points too close to each other isn't an issue — they should lead to some very thin triangles in the output, but they won't break the topology of the resulting mesh. However, in practice we lack the floating-point precision to accurately compute these thin triangles (which is what leads to ugly artifacts). On the other hand, this time our goal is not to compute something as precise as we can, but to visualize the data. In practice, nobody will see these thin triangles, simply because they're too thin.

Which is to say it's OK if we simply don't render them. Meaning it's OK if we dont even generate them. Meaning it's OK if we just filter out the input points that are too close. But how close is too close?

Once again, slapping an arbitrary epsilon is usually a bad solution, though in this specific case it's probably not bad, but just meh. There are ways to find a good epsilon that fits this specific use case:

- Knowing your maximal scale/zoom and pixel size, compute the distance which will map to less than half a pixel, and use that as an epsilon for filtering out points
- Knowing what exactly your algorithm does, and where the imprecision comes from, estimate the minimum separation between points that leads to acceptable floating-point errors, and use it as your epsilon
- Use a binary search to find a good epsilon by testing it against your dataset of input data
- Use your decades of floating-point experience to just guess a good epsilon (but don't forget to document this)

Unless you chose the last option, I can guarantee you that the correct value won't be `1e-4` or `1e-6`.

## Case in study: writing test cases

That's probably the most obvious one. If I'm writing a maths library, I want extensive test coverage. Tests will have to check if some function returns the value we expected, meaning it will have to compare the result with some reference value. But due to floating-point errors, the result will almost always differ.

Now, there are two ways we can do this. Option 1 is to assume exact IEEE754 conformance and write tests using equality comparisons. Even if there's some rounding involved, it must be the same on all conformant hardware (if the CPU flags are set correctly), so you can safely do the equality test. In many cases you can craft input data such that no rounding will be involved altogether!

In many functions (e.g. vector addition, subtraction, multiplication) you can just use integer coordinates (many of which are exactly representable as floats), or integers divided by a power of 2. For some cases it isn't enough: for example, when computing vector length, even if the coordinates are integers, the result might be an irrational number.

Even in this case we can cheat a bit and use [Pythagorean triples](https://en.wikipedia.org/wiki/Pythagorean_triple) to craft test cases where the length is known to be exactly representable in floating-point, for example

```cpp
length(vec2(3.f, 4.f)) == 5.f
length(vec2(5.f, 12.f)) == 13.f
length(vec2(0.4375f, 1.5f)) == 1.5625f
```

This is rather tiresome, as we'll have to craft special increasingly complicated tests for all our code. What's option 2, then?

Use epsilons! Be sure to use rather small epsilons, e.g. `FLT_EPSILON` or like, but it's honestly a good solution for this case. For the most part, it's very hard to break a maths library in such a way that epsilon-comparisons won't catch that.

However, note that if some of your functions provide additional guarantees (like `length` only being zero for a vector which is exactly zero, or `left_turn` being invariant under cycling the arguments), it's best to write separate specialized tests for these guarantees.

## To epsilon or not to epsilon

So, are epsilons good or bad? Usually bad, but sometimes okay. Is all your epsilon-driven code gonna break suddenly, now that you've read this post? Probably not.

Look, in many real-life use-cases all that doesn't matter. If you're writing a general-purpose high-quality maths library, you're obliged to care about this stuff. If you're goofying a toy physics engine for a squishy platformer game, epsilons will probably suit you well. And if they break, just replace `1e-4` with `2e-4` and be on your way.

The real answer to any engineering problem is not to follow a cult or a random internet person, but to think with your own brain. Shocking, I know. Nevertheless, I hope you learnt something!
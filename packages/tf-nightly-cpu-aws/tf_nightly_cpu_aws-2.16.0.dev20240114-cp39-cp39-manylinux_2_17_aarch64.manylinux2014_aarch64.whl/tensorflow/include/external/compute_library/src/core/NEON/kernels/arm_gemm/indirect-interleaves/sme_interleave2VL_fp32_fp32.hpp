/*
 * Copyright (c) 2022-2023 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#if defined(__ARM_FEATURE_SVE)

template <>
void interleave_block<2, 1, VLType::SME, false>(
  float * &out, const float * const *in,
  size_t width, size_t height, size_t row_offset, bool first
)
{
  ARM_COMPUTE_UNUSED(first);

  __asm__ __volatile__(
      ".inst 0xd503477f  // SMSTART ZA\n"
      "mov x22, %x[width]\n"
      "incw x22\n"
      "cntw x16\n"
      "sub x22, x22, #0x1\n"
      "udiv x22, x22, x16\n"  // n_passes = ceildiv(width, VL<T>)
      "mov x21, %x[width]\n"
      "sub x15, x16, #0x1\n"
      "sub x20, x22, #0x1\n"
      "ands x15, x21, x15\n"
      "sub x14, x16, #0x2\n"
      "mov x13, #0x0\n"
      "mov x11, %x[in]\n"
      "ldr x10, [x11, #0x0]\n"
      "add x9, %x[in], x16, LSL #3\n"
      "cntw x28, ALL, MUL #2\n"
      "ldr x27, [x9, #0x0]\n"
      "cntw x26, ALL, MUL #3\n"
      "lsr x20, x20, #0x1\n"  // n_loops = (n_passes - 1) / 2
      "ldr x25, [x11, #0x8]\n"
      "and x24, x22, #0x1\n"  // odd_tail = bool(n_passes & 0x1)
      "csel x15, x15, x16, NE\n"
      "ldr x23, [x9, #0x8]\n"
      "ptrue p13.s\n"
      "whilelt p12.s, XZR, %x[height]\n"
      "whilelt p11.s, x16, %x[height]\n"
      "mov x22, %x[row_offset]\n"
      "mov x21, %x[out]\n"
      "whilelt p10.s, x13, %x[width]\n"
      "whilelt p9.s, x13, %x[width]\n"
      "whilelt p8.s, x13, %x[width]\n"
      "add x11, x11, #0x10\n"
      "add x9, x9, #0x10\n"
      "mov x12, #0x0\n"
      "cbz x14, 2f\n"
      "1:"  // K loop: Charge: Loop
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960540  // ld1w { za0h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0xe0960364  // ld1w { za1h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      ".inst 0x25706581  // psel p1.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706160  // psel p0.s, p8.s/Z, p11.s[w12, #1]\n"
      "ldr x27, [x9, #0x0]\n"
      ".inst 0xe0960721  // ld1w { za0h.s[x12, #1] }, p1/Z, [x25, x22, LSL #2]\n"
      "ldr x25, [x11, #0x8]\n"
      "add x11, x11, #0x10\n"
      ".inst 0xe09602e5  // ld1w { za1h.s[x12, #1] }, p0/Z, [x23, x22, LSL #2]\n"
      "add x12, x12, #0x2\n"
      "cmp x12, x14\n"
      "ldr x23, [x9, #0x8]\n"
      "add x9, x9, #0x10\n"
      "blt 1b\n"
      "2:"  // K loop: Charge: End
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960540  // ld1w { za0h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      ".inst 0xe0960364  // ld1w { za1h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      ".inst 0x25706581  // psel p1.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706160  // psel p0.s, p8.s/Z, p11.s[w12, #1]\n"
      "mov x11, %x[in]\n"
      "add x9, %x[in], x16, LSL #3\n"
      ".inst 0xe0960721  // ld1w { za0h.s[x12, #1] }, p1/Z, [x25, x22, LSL #2]\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0xe09602e5  // ld1w { za1h.s[x12, #1] }, p0/Z, [x23, x22, LSL #2]\n"
      "ldr x27, [x9, #0x0]\n"
      "incw x22\n"
      "incw x13\n"
      "ldr x25, [x11, #0x8]\n"
      "add x11, x11, #0x10\n"
      "ldr x23, [x9, #0x8]\n"
      "add x9, x9, #0x10\n"
      "cbz x20, 8f\n"
      "mov x20, x20\n"
      "3:"  // K loop: Main loop
      "whilelt p9.s, x13, %x[width]\n"
      "whilelt p8.s, x13, %x[width]\n"
      "mov x12, #0x0\n"
      "cbz x14, 5f\n"
      "4:"  // K loop: Main loop: First: Loop
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960548  // ld1w { za2h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0xe096036c  // ld1w { za3h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      ".inst 0x25706580  // psel p0.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706162  // psel p2.s, p8.s/Z, p11.s[w12, #1]\n"
      "ldr x27, [x9, #0x0]\n"
      ".inst 0x25307541  // psel p1.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0960329  // ld1w { za2h.s[x12, #1] }, p0/Z, [x25, x22, LSL #2]\n"
      "ldr x25, [x11, #0x8]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0960aed  // ld1w { za3h.s[x12, #1] }, p2/Z, [x23, x22, LSL #2]\n"
      "ldr x23, [x9, #0x8]\n"
      ".inst 0xe0bf86a0  // st1w { za0v.s[x12] }, p1/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25707541  // psel p1.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0xe0b082a4  // st1w { za1v.s[x12] }, p0/Z, [x21, x16, LSL #2]\n"
      ".inst 0x25707540  // psel p0.s, p13.s/Z, p10.s[w12, #1]\n"
      "add x11, x11, #0x10\n"
      ".inst 0xe0bc86a1  // st1w { za0v.s[x12, #1] }, p1/Z, [x21, x28, LSL #2]\n"
      "add x9, x9, #0x10\n"
      ".inst 0xe0ba82a5  // st1w { za1v.s[x12, #1] }, p0/Z, [x21, x26, LSL #2]\n"
      "add x12, x12, #0x2\n"
      "cmp x12, x14\n"
      "addvl x21, x21, #4\n"
      "blt 4b\n"
      "5:"  // K loop: Main loop: First: Tail
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960548  // ld1w { za2h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      ".inst 0xe096036c  // ld1w { za3h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      "mov x11, %x[in]\n"
      "add x9, %x[in], x16, LSL #3\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0x25706580  // psel p0.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706161  // psel p1.s, p8.s/Z, p11.s[w12, #1]\n"
      ".inst 0xe0960329  // ld1w { za2h.s[x12, #1] }, p0/Z, [x25, x22, LSL #2]\n"
      "ldr x27, [x9, #0x0]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe09606ed  // ld1w { za3h.s[x12, #1] }, p1/Z, [x23, x22, LSL #2]\n"
      "ldr x25, [x11, #0x8]\n"
      ".inst 0x25307542  // psel p2.s, p13.s/Z, p10.s[w12]\n"
      "ldr x23, [x9, #0x8]\n"
      ".inst 0xe0bf82a0  // st1w { za0v.s[x12] }, p0/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25707541  // psel p1.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0x25707540  // psel p0.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0xe0b08aa4  // st1w { za1v.s[x12] }, p2/Z, [x21, x16, LSL #2]\n"
      "whilelt p10.s, x13, %x[width]\n"
      "incw x13\n"
      ".inst 0xe0bc86a1  // st1w { za0v.s[x12, #1] }, p1/Z, [x21, x28, LSL #2]\n"
      "add x11, x11, #0x10\n"
      "add x9, x9, #0x10\n"
      ".inst 0xe0ba82a5  // st1w { za1v.s[x12, #1] }, p0/Z, [x21, x26, LSL #2]\n"
      "addvl x21, x21, #4\n"
      "incw x22\n"
      "whilelt p9.s, x13, %x[width]\n"
      "whilelt p8.s, x13, %x[width]\n"
      "mov x12, #0x0\n"
      "cbz x14, 7f\n"
      "6:"  // K loop: Main loop: Second: Loop
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960540  // ld1w { za0h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0xe0960364  // ld1w { za1h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      ".inst 0x25706580  // psel p0.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706162  // psel p2.s, p8.s/Z, p11.s[w12, #1]\n"
      "ldr x27, [x9, #0x0]\n"
      ".inst 0x25307541  // psel p1.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0960321  // ld1w { za0h.s[x12, #1] }, p0/Z, [x25, x22, LSL #2]\n"
      "ldr x25, [x11, #0x8]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0960ae5  // ld1w { za1h.s[x12, #1] }, p2/Z, [x23, x22, LSL #2]\n"
      "ldr x23, [x9, #0x8]\n"
      ".inst 0xe0bf86a8  // st1w { za2v.s[x12] }, p1/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25707541  // psel p1.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0xe0b082ac  // st1w { za3v.s[x12] }, p0/Z, [x21, x16, LSL #2]\n"
      ".inst 0x25707540  // psel p0.s, p13.s/Z, p10.s[w12, #1]\n"
      "add x11, x11, #0x10\n"
      ".inst 0xe0bc86a9  // st1w { za2v.s[x12, #1] }, p1/Z, [x21, x28, LSL #2]\n"
      "add x9, x9, #0x10\n"
      ".inst 0xe0ba82ad  // st1w { za3v.s[x12, #1] }, p0/Z, [x21, x26, LSL #2]\n"
      "add x12, x12, #0x2\n"
      "cmp x12, x14\n"
      "addvl x21, x21, #4\n"
      "blt 6b\n"
      "7:"  // K loop: Main loop: Second: Tail
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      ".inst 0xe0960540  // ld1w { za0h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      ".inst 0xe0960364  // ld1w { za1h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      "mov x11, %x[in]\n"
      "add x9, %x[in], x16, LSL #3\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0x25706580  // psel p0.s, p9.s/Z, p12.s[w12, #1]\n"
      ".inst 0x25706161  // psel p1.s, p8.s/Z, p11.s[w12, #1]\n"
      ".inst 0xe0960321  // ld1w { za0h.s[x12, #1] }, p0/Z, [x25, x22, LSL #2]\n"
      "ldr x27, [x9, #0x0]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe09606e5  // ld1w { za1h.s[x12, #1] }, p1/Z, [x23, x22, LSL #2]\n"
      "ldr x25, [x11, #0x8]\n"
      ".inst 0x25307542  // psel p2.s, p13.s/Z, p10.s[w12]\n"
      "ldr x23, [x9, #0x8]\n"
      ".inst 0xe0bf82a8  // st1w { za2v.s[x12] }, p0/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25707541  // psel p1.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0x25707540  // psel p0.s, p13.s/Z, p10.s[w12, #1]\n"
      ".inst 0xe0b08aac  // st1w { za3v.s[x12] }, p2/Z, [x21, x16, LSL #2]\n"
      "whilelt p10.s, x13, %x[width]\n"
      "subs x20, x20, #0x1\n"
      ".inst 0xe0bc86a9  // st1w { za2v.s[x12, #1] }, p1/Z, [x21, x28, LSL #2]\n"
      "add x11, x11, #0x10\n"
      "add x9, x9, #0x10\n"
      ".inst 0xe0ba82ad  // st1w { za3v.s[x12, #1] }, p0/Z, [x21, x26, LSL #2]\n"
      "addvl x21, x21, #4\n"
      "incw x13\n"
      "incw x22\n"
      "bgt 3b\n"
      "8:"  // K loop: Tails
      "cbnz x24, 11f\n"
      "mov x11, %x[in]\n"
      "whilelt p9.s, x13, %x[width]\n"
      "whilelt p8.s, x13, %x[width]\n"
      "mov x12, #0x0\n"
      "9:"  // K loop: Tails: Even: First
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0bf82a0  // st1w { za0v.s[x12] }, p0/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0b082a4  // st1w { za1v.s[x12] }, p0/Z, [x21, x16, LSL #2]\n"
      "ldr x10, [x11, #0x0]\n"
      ".inst 0x25306581  // psel p1.s, p9.s/Z, p12.s[w12]\n"
      ".inst 0x25306160  // psel p0.s, p8.s/Z, p11.s[w12]\n"
      "ldr x27, [x11, x16, LSL #0x3]\n"
      ".inst 0xe0960548  // ld1w { za2h.s[x12] }, p1/Z, [x10, x22, LSL #2]\n"
      "add x11, x11, #0x8\n"
      "addvl x21, x21, #2\n"
      ".inst 0xe096036c  // ld1w { za3h.s[x12] }, p0/Z, [x27, x22, LSL #2]\n"
      "add x12, x12, #0x1\n"
      "cmp x12, x16\n"
      "blt 9b\n"
      "whilelt p10.s, x13, %x[width]\n"
      "whilelt p9.s, x13, %x[width]\n"
      "whilelt p8.s, x13, %x[width]\n"
      "mov x12, #0x0\n"
      "10:"  // K loop: Tails: Even: Second
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0bf82a8  // st1w { za2v.s[x12] }, p0/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0b082ac  // st1w { za3v.s[x12] }, p0/Z, [x21, x16, LSL #2]\n"
      "add x12, x12, #0x1\n"
      "cmp x12, x15\n"
      "addvl x21, x21, #2\n"
      "blt 10b\n"
      "whilelt p10.s, x13, %x[width]\n"
      "b 13f\n"
      "11:"  // K loop: Tails: Odd
      "mov x12, #0x0\n"
      "12:"  // K loop: Tails: Odd: Loop
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0bf82a0  // st1w { za0v.s[x12] }, p0/Z, [x21, XZR, LSL #2]\n"
      ".inst 0x25307540  // psel p0.s, p13.s/Z, p10.s[w12]\n"
      ".inst 0xe0b082a4  // st1w { za1v.s[x12] }, p0/Z, [x21, x16, LSL #2]\n"
      "add x12, x12, #0x1\n"
      "cmp x12, x15\n"
      "addvl x21, x21, #2\n"
      "blt 12b\n"
      "13:"  // K loop: End
      "mov %x[out], x21\n"
      ".inst 0xd503467f  // SMSTOP\n"
      : [out] "+&r" (out)
      : [height] "r" (height), [in] "r" (in), [row_offset] "r" (row_offset), [width] "r" (width)
      : "cc", "memory", "p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15", "x9", "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "z0", "z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8", "z9", "z10", "z11", "z12", "z13", "z14", "z15", "z16", "z17", "z18", "z19", "z20", "z21", "z22", "z23", "z24", "z25", "z26", "z27", "z28", "z29", "z30", "z31"
    );
}

#endif  // defined(__ARM_FEATURE_SVE)

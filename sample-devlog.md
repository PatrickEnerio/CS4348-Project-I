# 09-21-2026 10:18am

This is a sample devlog.
To demonstrate how a devlog should be written, I will be keeping one for a couple sessions of a project I am already in the middle of.
I am writing a computer simulator to be used for a demonstration in my 4337 class.
I am using Haskell, a functional programming language, for this project.
I have already implemented a way to represent instructions, encode and decode them as bytes, and have tested all instructions that do not need to access memory.
I will be picking up from here.

For the next step I need to implement memory.
I Plan to use a vector of bytes to represent memory, but am still debating if I should go for a more general solution of a typeclass (similar to an interface) in case I want to change the representation later.
 Just using a vector seems simpler, and I do not foresee myself changing the representation, but when possible and efficient is is often a good idea to thing more generally, especially in functional programming.

 # 09-21 3:58pm

 I've decided to go the more general route with Memory.
 It will not complicate the interface much, and usually in functional programming, more general the better.
 Another question came to me as I was thinking about this.
 My instruction decoder takes a list of bytes, and decodes them into a function.
 I wondered if I should modify them to take a memory and address, but due to haskell laziness and optimizations, the overhead of slicing a vector and converting to a list of bytes should be minimal.

 This session I plan to design the Memory typeclass and implement memory as a vector of bytes.
 This should hopefully be straight forward.

 # 09-21 5:03pm

 I finished the implementation I set out to do, but when I went to test it I discovered a strange bug in my code that packs/unpacks words.
 The simulated machine is 16bit, so I have functions that convert two bytes to a 16bit word and a 16-bit word to two bytes, but the conversion is not happening properly.
 I also discovered another bug that I had introduced earlier in my CPU code.
 This is due to some refactoring I did, and I will need to take some time to look at it.
 My next session will be dedicated to solving these two bugs and testing memory.

# 09-21 5:09pm

I realized my mistake when packing/unpacking words.
The problem was with the bit shift function.
I had the directions backwards.
This is what I thought it was, but after fixing it I still was having a problem.
It turns out that since I had that code in a library, separate from my application code, the repl was only recompiling my application code and not the library.
So, the code never changed.
A quick recompile of the library code shows the bug was fixed.
Next session I just need to focus on the CPU bug, and testing memory.

# 09-22 4:29pm

The function that modifies the state, representing the execution of an instruction, was originally a pure function, but I refactored to make it monadic because the interface was nicer.
I missed a place or two where the function is called.
So, I either have to change those function to be monadic or change the way they interact so that they can remain pure.
It will likely be the former.

This session I will fix the CPU bug, and finish testing for Memory.

# 09-22 4:55pm

Fixing the bug was simpler than I thought.
Turned out it was only affecting test code at the moment.
I switched the calling function to a monadic function.

I've tested the Memory, and it looks like it is working well.
I decided to add a new function to the type class that will write a list of bytes to memory starting at some address.
This will make writing programs, which will be a list of bytes to memory, simpler.
I encoded an instruction, wrote the bytes to memory, then read the bytes from memory and decoded them.
I got the original instruction back.
So, memory should be working.

My next session I will add a memory to the system state, will be expanding the CPU simulator to execute instructions that need access to memory to work.

# NOTES

This is not part of the devlog, and contain notes that may be helpful when approaching your own dev log.

- This devlog is incomplete.
  I only have 2 sessions, and of course there is more work to be done for the project.
- Do not forget to commit the changes every time you add an entry.
  This timestamps your entry along with your progress with the code.
- There is no length requirement, but as can be seen from my example, 2-3 paragraphs will likely be needed to talk about all your relevant thoughts.
  Just keep in mind, that you will be graded on the content.
  Do you demonstrate an understanding of the project topic?
- Overall the point is to record your thoughts.
  Notice 09-21 3:58pm I talk about thinking about making some changes to existing code, but decided against it.
  These thoughts are work, and should be recorded.
- Notice 09-21 5:09pm was done outside a session. This is okay.
  If you need to make a quick note like this add the entry and then commit the changes.
  It is important to write down your thought as soon as possible.
  If you wait too long, you may forget.
- Feel free to come back later and clean up the devlog, modifying or even adding/clarifying content.
  These changes will be tracked by your git repository.
  But the first pass should definitely be done as you work (as instructed in the general  instructions).

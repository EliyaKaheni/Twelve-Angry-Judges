using System;
using System.Collections.Generic;
using System.Threading;

namespace Extensions
{
    public static class ShuffleExtension
    {
        public static class ThreadSafeRandom
        {
            [ThreadStatic] private static Random _local;

            public static Random ThisThreadsRandom
            {
                get { return _local ??= new Random(unchecked(Environment.TickCount * 31 + Thread.CurrentThread.ManagedThreadId)); }
            }
        }
        
        public static void Shuffle<T>(this IList<T> list)
        {
            var n = list.Count;
            while (n > 1)
            {
                n--;
                var k = ThreadSafeRandom.ThisThreadsRandom.Next(n + 1);
                (list[k], list[n]) = (list[n], list[k]);
            }
        }
    }
}

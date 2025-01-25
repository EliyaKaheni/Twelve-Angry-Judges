using System;
using System.Collections.Generic;
using Extensions;
using UnityEngine;
using Random = UnityEngine.Random;

namespace Judges
{
    [CreateAssetMenu(fileName = "JudgeAppearance", menuName = "Scriptable Objects/JudgeAppearance")]
    public class JudgeAppearanceContainer : ScriptableObject
    {
        public List<Sprite> Avatars;
        public List<string> Names;
        public List<string> Traits;

        public void FillNamesAndTraits()
        {
            var names = "Ashcroft, Barrington, Coldwell, Dunsmore, Eversfield, Fenwick, Gainsborough, Harcourt, Inglewood, Jameston, Kensington, Lockridge, Middlebrook, Newcomb, Ormsby, Prescott, Ravensworth, Shelbourne, Taverner, Uxbridge, Vassel, Wainwright, Yelverton, Aldridge, Blackwood, \nAbernathy, Bellamy, Cardwell, Danforth, Ellsworth, Fairchild, Grimsby, Haverford, Iverson, Kingsley, Laughton, Merriweather, Norwood, Oakwood, Penrose, Quimby, Rockwell, Stanhope, Thistledown, Underhill, Varden, Whitaker, Yardley, Zeller, Crowhurst";
            Names = new List<string>(names.Split(", ", StringSplitOptions.RemoveEmptyEntries));

            var traits = "\nFair, Honest, Impartial, Diligent, Wise, Patient, Empathetic, Objective, Prudent, Decisive, Biased, Prejudiced, Favoritist, Bribable, Nepotistic, Lazy, Rash, Ignorant, Vindictive, Greedy";
            Traits = new List<string>(traits.Split(", ", StringSplitOptions.RemoveEmptyEntries));
        }

        public JudgeAppearance GetRandomAppearance()
        {
            var avatar = Avatars[Random.Range(0, Avatars.Count)];
            var name = Names[Random.Range(0, Names.Count)];


            Traits.Shuffle();
            var traits = "";

            var min = Mathf.Min(3, Traits.Count);
            for (var i = 0; i < min; i++)
            {
                traits += Traits[i];

                if (i < min - 1)
                    traits += ", ";
                else
                    traits += ".";
            }
            
            return new JudgeAppearance { Avatar =  avatar, Name = name, Traits = traits };
        }
    }
}
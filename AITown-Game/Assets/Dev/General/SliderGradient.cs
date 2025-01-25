using UnityEngine;
using UnityEngine.UI;

namespace General
{
    public class SliderGradient : MonoBehaviour
    {
        [SerializeField] private Slider slider;
        [SerializeField] private Image sliderFill;
        [SerializeField] private Gradient gradient;
        
        public void Update()
        {
            var value = slider.value;
            sliderFill.color = gradient.Evaluate(value);
        }
    }
}

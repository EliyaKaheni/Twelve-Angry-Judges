using UnityEngine;
using UnityEngine.UI;

namespace General
{
    public class VerticalLayoutGroupContent : MonoBehaviour
    {
        [SerializeField] private RectTransform rectTransform;
        [SerializeField] private float childHeight;
        [SerializeField] private float spacing;

        private Button[] _children;

        private void Awake()
        {
            _children = transform.GetComponentsInChildren<Button>();
        }

        public void Update()
        {
            Refresh();
        }

        public void Refresh()
        {
            var childCount = _children.Length;
            var height = (childHeight + spacing) * childCount;
            
            rectTransform.sizeDelta = new Vector2(rectTransform.sizeDelta.x, height);
        }
    }
}

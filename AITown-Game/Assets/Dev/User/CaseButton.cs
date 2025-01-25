using Cases;
using TMPro;
using UnityEngine;

namespace User
{
    public class CaseButton : MonoBehaviour
    {
        [SerializeField] private TMP_Text title;
        
        private UserPanel _userPanel;
        private CaseData _caseData;
        
        public void Initialize(UserPanel userPanel, CaseData caseData)
        {
            _userPanel = userPanel;
            _caseData = caseData;
            title.text = _caseData.CaseName;
        }
        
        public void ShowCase()
        {
            _userPanel.ShowCase(_caseData);
        }
    }
}

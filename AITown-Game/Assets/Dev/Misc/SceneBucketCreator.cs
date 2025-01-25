using Mosaic.Feather.Runtime.DependencyLocation;
using Mosaic.Feather.Runtime.Settings;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Misc
{
    [DefaultExecutionOrder(-11000)]
    public class SceneBucketCreator : MonoBehaviour
    {
        private void Awake()
        {
            var bucketIdentifier = SceneManager.GetActiveScene();
            FeatherDL.CreateBucket(bucketIdentifier);
            Debug.Log($"Scene bucket created: {bucketIdentifier.buildIndex}, {bucketIdentifier.name}");
        }
    }
}

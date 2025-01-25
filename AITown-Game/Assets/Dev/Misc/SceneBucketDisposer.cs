using Mosaic.Feather.Runtime.DependencyLocation;
using Mosaic.Feather.Runtime.Settings;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Misc
{
    [DefaultExecutionOrder(+11000)]
    public class SceneBucketDisposer : MonoBehaviour
    {
        private void OnDestroy()
        {
            var bucketIdentifier = SceneManager.GetActiveScene();
            FeatherDL.DisposeBucket(bucketIdentifier);
            Debug.Log($"Scene bucket disposed: {bucketIdentifier.buildIndex}, {bucketIdentifier.name}");
        }
    }
}

import * as aws from "@pulumi/aws";

// Create a bucket and expose a website index document
export const sourceBucket = new aws.s3.Bucket("nuage-source-bucket", {});
